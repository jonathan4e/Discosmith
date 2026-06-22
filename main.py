#main.py - Discosmith
import sys
import json
import os
import socket
from PySide6.QtCore import Qt, QSize, QTimer, QRect, QUrl, QStandardPaths, QThread, Signal
from PySide6.QtGui import QPainter, QImage, QBrush, QColor, QFont, QDesktopServices
from PySide6.QtWidgets import QApplication
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from qfluentwidgets import FluentWindow, FluentIcon as FIF, NavigationItemPosition, SplashScreen, NavigationWidget, isDarkTheme
from dashboard import dashboard
from settings import settings


#note - ai was used in helping me learn a part of the code below.
class LocalhostTokenListener(QThread):
    token_received = Signal(str)

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind(('127.0.0.1', 14525))
            server.listen(1)
            conn, addr = server.accept()
            request = conn.recv(1024).decode('utf-8')
            
            if "access_token=" in request:
                query_line = request.split(' ')[1]
                params = query_line.split('?')[1]
                param_dict = dict(item.split('=') for item in params.split('&') if '=' in item)
                token = param_dict.get("access_token")
                if token:
                    self.token_received.emit(token)
            
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n\r\n"
                "<html><body style='font-family:sans-serif; text-align:center; padding-top:50px; background:#111827; color:#f3f4f6;'>"
                "<h1>Login Successful!</h1><p>You can close this tab and return to DiscoSmith.</p>"
                "</body></html>"
            )
            conn.sendall(response.encode('utf-8'))
            conn.close()
        except Exception as e:
            print(e)
        finally:
            server.close()


class AvatarWidget(NavigationWidget):
    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.username = "Guest Account"
        self.is_logged_in = False
        self.set_avatar_image(None)

    def set_avatar_image(self, image_data=None):
        if image_data:
            img = QImage.fromData(image_data)
        else:
            img = QImage(24, 24, QImage.Format_ARGB32)
            img.fill(QColor(140, 140, 140))
        self.avatar = img.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()

    def update_user_info(self, username, logged_in=True):
        self.username = username
        self.is_logged_in = logged_in
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        if self.isPressed: painter.setOpacity(0.7)
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 15))
            painter.drawRoundedRect(self.rect(), 5, 5)
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)
        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            painter.setFont(QFont('Segoe UI', 9))
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, self.username)

class MainWindow(FluentWindow):
    VERCEL_AUTH_URL = "https://discosmith-oauth.vercel.app/api/auth" 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DiscoSmith")
        
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(120, 120))
        self.splashScreen.show()

        self.appdata_dir = os.path.join(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation), "discosmith")
        os.makedirs(self.appdata_dir, exist_ok=True)
        self.config_file = os.path.join(self.appdata_dir, "session.json")

        self.network_manager = QNetworkAccessManager(self)
        self.listener_thread = None
        self.check_saved_login()

        self.resize(1000, 700)

        QTimer.singleShot(1500, self.splashScreen.finish)

    def initNavigation(self):
        self.settings = settings()
        self.dashboard = dashboard()
        self.avatar_widget = AvatarWidget(self)
        self.addSubInterface(self.dashboard, FIF.HOME, "Dashboard")
        self.navigationInterface.addSeparator()
        self.navigationInterface.addWidget(
            routeKey='avatar', widget=self.avatar_widget, onClick=self.handle_avatar_click, position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(self.settings, FIF.SETTING, "Settings", NavigationItemPosition.BOTTOM)
        self.show()

    def handle_avatar_click(self):
        if hasattr(self, 'avatar_widget') and self.avatar_widget.is_logged_in: return

        self.listener_thread = LocalhostTokenListener()
        self.listener_thread.token_received.connect(self.on_token_received)
        self.listener_thread.start()

        QDesktopServices.openUrl(QUrl(self.VERCEL_AUTH_URL))

    def on_token_received(self, token):
        self.save_session(token)
        self.fetch_discord_profile(token)

    def save_session(self, token):
        with open(self.config_file, "w") as f: json.dump({"access_token": token}, f)

    def check_saved_login(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                token = json.load(f).get("access_token")
                if token: 
                    self.fetch_discord_profile(token)
                else:
                    self.handle_avatar_click()
        else:
            self.handle_avatar_click()

    def fetch_discord_profile(self, token):
        request = QNetworkRequest(QUrl("https://discord.com/api/users/@me"))
        request.setRawHeader(b"Authorization", f"Bearer {token}".encode())
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self.on_profile_fetched(reply))

    def on_profile_fetched(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            try:
                data = json.loads(reply.readAll().data().decode())
                if not hasattr(self, 'dashboard'):
                    self.initNavigation()
                self.avatar_widget.update_user_info(data.get("username", "Discord User"), logged_in=True)
                
                user_id, avatar_hash = data.get("id"), data.get("avatar")
                if user_id and avatar_hash:
                    self.fetch_avatar_image(f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=32")
            except: pass
        else:
            self.handle_avatar_click()
        reply.deleteLater()

    def fetch_avatar_image(self, url_str):
        reply = self.network_manager.get(QNetworkRequest(QUrl(url_str)))
        reply.finished.connect(lambda: [self.avatar_widget.set_avatar_image(reply.readAll().data()), reply.deleteLater()])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())