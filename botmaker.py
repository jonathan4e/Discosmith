from PySide6.QtWidgets import QFrame, QVBoxLayout, QStackedWidget, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor
import os
import sys
from qfluentwidgets import LineEdit, SingleDirectionScrollArea,  PrimaryPushButton, BodyLabel, CaptionLabel, TransparentToolButton, CardWidget, MessageBox, FluentIcon as FIF, PrimaryDropDownToolButton, RoundMenu, TitleLabel, Action
import json
from boteditor import boteditor
import shutil

class newbot(MessageBox):
    def __init__(self, parent=None):
        super().__init__("Add Bot", "Enter bot name:", parent)
        self.name = LineEdit(self)
        self.name.setPlaceholderText("DiscoBot")
        self.name.setClearButtonEnabled(True)
        self.textLayout.addWidget(self.name)
        self.widget.setMinimumWidth(400)

class bottoken(MessageBox):
    def __init__(self, parent=None):
        super().__init__("Bot token", "Enter bot token:", parent)
        self.token = LineEdit(self)
        self.token.setPlaceholderText("MTxxxxx....")
        self.token.setClearButtonEnabled(True)
        self.textLayout.addWidget(self.token)  
        self.widget.setMinimumWidth(400)




class botslist(CardWidget):
    def __init__(self, bot_name, parent_maker, parent=None):
        super().__init__(parent)
        self.setObjectName("botslist")
        self.bot_name = bot_name
        self.parent_maker = parent_maker
        self.hlayout = QHBoxLayout(self)
        self.vlayout = QVBoxLayout()

        self.botlogo = TransparentToolButton(FIF.ROBOT, self)
        self.botlogo.setFixedSize(48, 48)
        self.botlogo.setIconSize(QSize(28, 28))


        self.title = BodyLabel(bot_name, self)
        self.subtitle = CaptionLabel(f"{os.getcwd()}", self)

        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.addSpacing(2)
        self.vlayout.addWidget(self.title,0, Qt.AlignVCenter)
        self.vlayout.addWidget(self.subtitle,0, Qt.AlignVCenter)

        self.open = PrimaryPushButton("Open", self)
        self.open.clicked.connect(self.openbot)

        self.more = TransparentToolButton(FIF.MORE, self)
        self.more.setFixedSize(32,32)

        self.menu = RoundMenu(parent=self.more)
        deleteicon = FIF.DELETE.icon(color = QColor(255,77,79))  #used ai to determine this specific shade
        self.deleteaction = Action(deleteicon, "Delete", self, triggered=self.delete)
        self.menu.addAction(self.deleteaction)
        self.more.clicked.connect(lambda: self.menu.exec(self.more.mapToGlobal(self.more.rect().bottomLeft())))

        self.hlayout.setContentsMargins(15,12,5,12)
        self.hlayout.setSpacing(15)
        self.hlayout.addWidget(self.botlogo,0, Qt.AlignVCenter)
        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addStretch(1)
        self.hlayout.addWidget(self.open,0, Qt.AlignRight | Qt.AlignVCenter)
        self.hlayout.addWidget(self.more,0, Qt.AlignRight | Qt.AlignVCenter)
    

    def openbot(self):
        self.parent_maker.loadbot(self.bot_name)
    
    def delete(self):
        deleteconfirmation = MessageBox("Delete Bot", f"Are you sure you want to permanently delete bot {self.bot_name}?", self.parent_maker.window())
        deleteconfirmation.yesButton.setText("Yes, Delete")
        deleteconfirmation.cancelButton.setText("Cancel")

        if deleteconfirmation.exec():
            botpath = os.path.join(self.parent_maker.root, self.bot_name)
            shutil.rmtree(botpath)

        self.parent_maker.loadbotsincardwidget()



class botmaker(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("botmaker")
        self.root = os.path.abspath(os.getcwd())
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


        self.scrollarea = SingleDirectionScrollArea(orient=Qt.Vertical, parent=self)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setFrameShape(QFrame.NoFrame)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollarea.setStyleSheet("QScrollArea{background: transparent; border: none}")

        self.scrollwidget = QWidget()
        self.scrollwidget.setStyleSheet("QWidget{background: transparent}")

        self.scrollayout = QVBoxLayout(self.scrollwidget)
        self.scrollayout.setContentsMargins(0,10,0,10)
        self.scrollayout.setSpacing(10)
        self.scrollayout.setAlignment(Qt.AlignTop)
        self.scrollarea.setWidget(self.scrollwidget)

        layout2.addWidget(self.scrollarea)


        self.editor = boteditor(self)
        self.stacked_widget.addWidget(self.bothome) 
        self.stacked_widget.addWidget(self.editor)

        self.loadbotsincardwidget()


    def loadbotsincardwidget(self):
        os.chdir(self.root)
        ignored = {"__pycache__", ".venv", ".idea", ".vscode", ".github", ".git"}

        for item in os.listdir(self.root):
            item_path = os.path.join(self.root, item)
            if os.path.isdir(item_path) and item not in ignored:
                card = botslist(item, self, self.scrollwidget)
                self.scrollayout.addWidget(card)

    def loadbot(self, bot_name):
        os.chdir(self.root)
        self.editor.setdir(bot_name)
        self.editor.setbotname(bot_name)
        self.stacked_widget.setCurrentWidget(self.editor)



    def showbotname(self):
        dialog = newbot(self)
        if dialog.exec():
            bot_name = dialog.name.text().strip()
            if bot_name:
                self.bot_name = bot_name
                os.makedirs(f"{bot_name}", exist_ok=True)
                env_path = os.path.join(bot_name, ".env")
                dialog2 = bottoken(self)
                dialog2.exec()
                token = dialog2.token.text().strip()
                if token:
                    with open(env_path, "w") as f:
                        f.write(f"DISCORD_BOT_TOKEN={token}\nGEMINI_API_KEY=\nWELCOMER=FALSE\nAI=FALSE\nGA=FALSE\nMOD=FALSE\nMUSIC=FALSE\nJOKE=FALSE\nRPS=FALSE\nQUOTE=FALSE\nREMINDER=FALSE\nCOIN=FALSE\nSERVERINFO=FALSE\nMEME=FALSE\nDICE=FALSE\nWEATHER=FALSE\n")
                else:
                    MessageBox.information(self, "Error", "Please enter a valid bot token.")
                if not os.path.exists(env_path):
                    with open(env_path, "w") as f:
                        f.write("") 
                        token = dialog2.token.text().strip()
                        if token:
                            with open(env_path, "w") as f:
                               f.write(f"DISCORD_BOT_TOKEN={token}\nGEMINI_API_KEY=\nWELCOMER=FALSE\nAI=FALSE\nGA=FALSE\nMOD=FALSE\nMUSIC=FALSE\nJOKE=FALSE\nRPS=FALSE\nQUOTE=FALSE\nREMINDER=FALSE\nCOIN=FALSE\nSERVERINFO=FALSE\nMEME=FALSE\nDICE=FALSE\nWEATHER=FALSE\n")
                        else:
                            MessageBox.information(self, "Error", "Please enter a valid bot token.")
                self.editor.setdir(bot_name)
                self.editor.setbotname(bot_name)
                self.stacked_widget.setCurrentWidget(self.editor)
                
            else:
                MessageBox.information(self, "Error", "Please enter a valid bot name.")