from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Qt
import os
from qfluentwidgets import LineEdit, MessageBox, FluentIcon as FIF, PrimaryDropDownToolButton, RoundMenu, TitleLabel, Action


class newbot(MessageBox):
    def __init__(self, parent=None):
        super().__init__("Add Bot", "Enter bot name:", parent)

        self.nameInput = LineEdit(self)
        self.nameInput.setPlaceholderText("DiscoBot")
        self.nameInput.setClearButtonEnabled(True)

        self.textLayout.addWidget(self.nameInput)

        self.widget.setMinimumWidth(400)


class dashboard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboard")
        self.title = TitleLabel("Dashboard")

        self.button = PrimaryDropDownToolButton(FIF.ADD,"Add")
        menu = RoundMenu(parent=self.button)
        menu.addAction(Action(FIF.ADD, "Add Bot", triggered=self.showbotname))
        self.button.setMenu(menu)


        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.button, alignment=Qt.AlignRight)
        layout.addStretch()
        self.setLayout(layout)


    def showbotname(self):
        dialog = newbot(self)
        if dialog.exec():
            bot_name = dialog.nameInput.text().strip()
            if bot_name:
                self.bot_name = bot_name
                os.makedirs(f"{bot_name}",exist_ok=True)