from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QApplication
from qfluentwidgets import FluentWindow, FluentIcon as FIF, NavigationItemPosition, setFont, SubtitleLabel, SplashScreen
import sys
from dashboard import dashboard

#temporary until i make the other pages
class Page(QFrame):
    def __init__(self, text, parent=None):
        
        super().__init__(parent)
        self.label = SubtitleLabel(text, self)

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)

        self.label.setAlignment(Qt.AlignCenter)
        setFont(self.label, 24)

        self.setObjectName(text.replace(" ", "_"))

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("DiscoSmith")
        self.setWindowIcon(QIcon("logo.png"))
        self.resize(1000,700)
        
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize = (QSize(120,120))
        self.splashScreen.show()

        self.settings = Page("Settings", self)
        self.dashboard = dashboard()
        self.initNavigation()

        QTimer.singleShot(3000, self.splashScreen.finish)
        self.show()

    def initNavigation(self):
        self.addSubInterface(self.dashboard, FIF.HOME, "Dashboard")
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.settings, FIF.SETTING, "Settings", NavigationItemPosition.BOTTOM)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())