from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtGui import QColor
from qfluentwidgets import TitleLabel, setTheme, Theme, SwitchSettingCard, SettingCardGroup, FluentIcon as FIF, PushSettingCard, setThemeColor, ColorDialog
import json
import os

class settings(QFrame):
    def __init__(self, configpath, parent=None):
        super().__init__(parent)
        self.setObjectName("settings")
        self.title = TitleLabel("Settings")
        self.configpath = configpath

        self.themecard = SwitchSettingCard(icon=FIF.BRUSH, title="Dark Mode", content="Change the theme of the app", parent=self)
        self.themecard.switchButton.setChecked(False)
        self.themecard.checkedChanged.connect(self.themechanged)

        self.accentcard = PushSettingCard(text = "Choose Color", icon=FIF.PALETTE, title="Accent Color", content="Change the primary accent colour", parent=self)
        self.accentcard.clicked.connect(self.opencolorpicker)

        self.personalization = SettingCardGroup("Personalization", self)
        self.personalization.addSettingCard(self.themecard)
        self.personalization.addSettingCard(self.accentcard)


        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 22, 36, 22)
        layout.setSpacing(10)

        layout.addWidget(self.title)
        layout.addSpacing(15)
        layout.addWidget(self.personalization)
        layout.addStretch()

        self.setLayout(layout)
        self.syncbuttons()

    def syncbuttons(self):
        if os.path.exists(self.configpath):
            try:
                with open(self.configpath, "r") as f:
                    data = json.load(f)

                    saved_theme = data.get("theme", "LIGHT")
                    dark = saved_theme in ["dark", "DARK"]
                    self.themecard.switchButton.blockSignals(True)
                    self.themecard.switchButton.setChecked(dark)
                    self.themecard.switchButton.blockSignals(False)
            except Exception as e:
                print(f"Error syncing settings buttons: {e}")


    def themechanged(self, checked):
        setTheme(Theme.DARK if checked else Theme.LIGHT)
        data = {}
        if os.path.exists(self.configpath):
            with open(self.configpath, "r") as f:
                data = json.load(f)
        data["theme"] = "DARK" if checked else "LIGHT"
        with open(self.configpath, "w") as f:
            json.dump(data, f, indent=4)

    
    def opencolorpicker(self):
        w = ColorDialog(QColor("#0078D4"), "Choose Accent Color", self.window(), enableAlpha=False)
        w.colorChanged.connect(self.colorchanged)
        w.exec()

    def colorchanged(self, color):
        setThemeColor(color)
        data={}
        if os.path.exists(self.configpath):
            with open(self.configpath, "r") as f:
                data = json.load(f)
        data["accent_color"] = color.name()
        
        with open(self.configpath, "w") as f:
            json.dump(data, f, indent=4)