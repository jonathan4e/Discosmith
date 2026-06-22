import os
import json
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import TitleLabel, SubtitleLabel, BodyLabel, LineEdit, SimpleCardWidget, SwitchButton, FluentWindow, MessageBox

class newbot(MessageBox):
    def __init__(self, parent=None):
        super().__init__("Bot Token", "Enter your Discord bot token:", parent)
        self.tokenInput = LineEdit(self)
        self.tokenInput.setPlaceholderText("MTxxxxxxxxxxxxxx...")
        self.tokenInput.setClearButtonEnabled(True)
        self.textLayout.addWidget(self.tokenInput)
        self.widget.setMinimumWidth(400)


class settingsCard(SimpleCardWidget):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        
        self.titleLabel = SubtitleLabel(title, self)
        self.descriptionL = BodyLabel(description, self)
        self.descriptionL.setTextColor(Qt.gray)
        
        self.switchBtn = SwitchButton(self)
        self.switchBtn.setOnText("Enabled")
        self.switchBtn.setOffText("Disabled")
        
        textLayout = QVBoxLayout()
        textLayout.addWidget(self.titleLabel)
        textLayout.addWidget(self.descriptionL)
        textLayout.addStretch()
        
        mainLayout = QHBoxLayout(self)
        mainLayout.addLayout(textLayout)
        mainLayout.addStretch()
        mainLayout.addWidget(self.switchBtn, alignment=Qt.AlignVCenter)
        self.setLayout(mainLayout)


class botmakerpage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("botmakerpage")
        self.bot_name = "Bot"
        
        self.title = TitleLabel("Bot Editor", self)
        self.sub1 = SubtitleLabel("Configuration Profile: ...", self)

        grid_layout = QGridLayout()
        cards_data = [
            ("Mod", "Adds mod functions for admin.", 0, 0),
            ("Welcome", "Greets new members when they join.", 0, 1),
            ("Music", "Enables YouTube/Spotify playback commands.", 1, 0),
            ("Economy", "Tracks virtual currency.", 1, 1)
        ]
        
        for title, description, row, col in cards_data:
            card = settingsCard(title, description, self)
            grid_layout.addWidget(card, row, col)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.sub1)
        main_layout.addSpacing(20)
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)
        
        self.load_config()


    def load_config(self):
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            self.bot_name = data.get("bot_name", "Unknown Bot")
            self.sub1.setText(f"Configuration Profile: {self.bot_name}")
        
        envpath = os.path.join(self.bot_name, ".env")
        token_found = False

        if os.path.exists(envpath):
            with open(envpath, "r") as f:
                content = f.read().strip()
                if "DISCORD_TOKEN=" in content:
                    lines = [line for line in content.splitlines() if line.startswith("DISCORD_TOKEN=")]
                    if lines and len(lines[0].split("=", 1)[1].strip()) > 0:
                        token_found = True

        if not token_found:
            token_dialog = newbot(self)
            if token_dialog.exec():
                token_value = token_dialog.tokenInput.text().strip()
                if token_value:
                    with open(env_path, "w") as f:
                        f.write(f"DISCORD_TOKEN={token_value}\n")
                else:
                    MessageBox("Error", "Token cannot be empty. Bot features may not work.", self).exec()


class mainbotmaker(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discosmith - Bot Editor")
        self.resize(800, 600)
        
        self.main_view = botmakerpage(self)
        self.addSubInterface(self.main_view, None, "Bot Config")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = mainbotmaker()
    sys.exit(app.exec())