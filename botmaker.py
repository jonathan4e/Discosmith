from PySide6.QtWidgets import QFrame, QVBoxLayout, QStackedWidget, QWidget
from PySide6.QtCore import Qt
import os
import sys
from qfluentwidgets import LineEdit, MessageBox, FluentIcon as FIF, PrimaryDropDownToolButton, RoundMenu, TitleLabel, Action
import json
from boteditor import boteditor

class newbot(MessageBox):
    def __init__(self, parent=None):
        super().__init__("Add Bot", "Enter bot name:", parent)
        self.name = LineEdit(self)
        self.name.setPlaceholderText("DiscoBot")
        self.name.setClearButtonEnabled(True)
        self.textLayout.addWidget(self.name)
        self.widget.setMinimumWidth(400)


class botmaker(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("botmaker")
        
        self.layout1 = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget(self)
        self.layout1.addWidget(self.stacked_widget)
        self.layout1.setContentsMargins(0, 0, 0, 0)

        self.bothome = QWidget()
        layout2 = QVBoxLayout(self.bothome)
        
        self.title = TitleLabel("Bot Editor")
        self.button = PrimaryDropDownToolButton(FIF.ADD, "Add")
        menu = RoundMenu(parent=self.button)
        menu.addAction(Action(FIF.ADD, "Add Bot", triggered=self.showbotname))
        self.button.setMenu(menu)

        layout2.addWidget(self.title)
        layout2.addWidget(self.button, alignment=Qt.AlignRight)
        layout2.addStretch()
        self.editor = boteditor(self)
        self.stacked_widget.addWidget(self.bothome) 
        self.stacked_widget.addWidget(self.editor)

    def showbotname(self):
        dialog = newbot(self)
        if dialog.exec():
            bot_name = dialog.name.text().strip()
            if bot_name:
                self.bot_name = bot_name
                os.makedirs(f"{bot_name}", exist_ok=True)
                env_path = os.path.join(bot_name, ".env")
                if not os.path.exists(env_path):
                    with open(env_path, "w") as f:
                        f.write("") 
                data = {"bot_name": bot_name}
                with open('data.json', 'w') as json_file:
                    json.dump(data, json_file)
                self.editor.setbotname(bot_name)
                self.stacked_widget.setCurrentWidget(self.editor)
                
            else:
                MessageBox.information(self, "Error", "Please enter a valid bot name.")