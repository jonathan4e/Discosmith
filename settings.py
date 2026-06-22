#settings.py - Discosmith
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout
from qfluentwidgets import TitleLabel, SwitchButton, setTheme, Theme, BodyLabel



class settings(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Settings")
        self.title = TitleLabel("Settings")

        button = SwitchButton()
        button.checkedChanged.connect(lambda checked: setTheme(Theme.DARK if checked else Theme.LIGHT))
        button.setChecked(True)
        label = BodyLabel("Dark Theme")

        toggle_layout = QHBoxLayout()
        toggle_layout.addWidget(label)
        toggle_layout.addWidget(button)
        toggle_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addSpacing(20)
        layout.addLayout(toggle_layout)
        layout.addStretch()
        self.setLayout(layout)