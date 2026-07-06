from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtGui import QColor
from qfluentwidgets import TitleLabel, setTheme, Theme, SwitchSettingCard, SettingCardGroup, FluentIcon as FIF, PushSettingCard, setThemeColor, ColorDialog

class settings(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settings")
        self.title = TitleLabel("Settings")

        self.themecard = SwitchSettingCard(icon=FIF.BRUSH, title="Dark Mode", content="Change the theme of the app", parent=self)
        self.themecard.switchButton.setChecked(False)
        self.themecard.checkedChanged.connect(lambda checked: setTheme(Theme.DARK if checked else Theme.LIGHT))

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

    def opencolorpicker(self):
        w = ColorDialog(QColor("#0078D4"), "Choose Accent Color", self.window(), enableAlpha=False)
        w.colorChanged.connect(lambda color: setThemeColor(color))
        w.exec()