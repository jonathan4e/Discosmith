from PySide6.QtWidgets import QFrame, QVBoxLayout, QStackedWidget, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
import os
import sys
from qfluentwidgets import LineEdit, MessageBox, FluentIcon as FIF, PrimaryDropDownToolButton, RoundMenu, TitleLabel, Action, SwitchButton, CardWidget, BodyLabel, CaptionLabel, TransparentToolButton
import json

class configCard(CardWidget):
    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent)
        self.title = BodyLabel(title, self)
        self.subtitle = CaptionLabel(subtitle, self)
        self.button = SwitchButton(self)
        self.more = TransparentToolButton(FIF.MORE, self)
        self.hlayout = QHBoxLayout(self)
        self.vlayout = QVBoxLayout()

        
        self.setFixedHeight(73)
        self.subtitle.setTextColor("#606060", "#d2d2d2")
        self.button.setFixedWidth(120)

        self.hlayout.setContentsMargins(20,11,11,11)
        self.hlayout.setSpacing(15)
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setSpacing(0)
        self.vlayout.addWidget(self.title,0, Qt.AlignVCenter)
        self.vlayout.addWidget(self.subtitle,0, Qt.AlignVCenter)
        self.vlayout.setAlignment(Qt.AlignVCenter)
        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addStretch(1)

        self.hlayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hlayout.addWidget(self.more,0, Qt.AlignRight)
        self.more.setFixedSize(32,32)

class boteditor(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.pagetitle = TitleLabel("Bot Editor")
        self.layout.addWidget(self.pagetitle)
        self.layout.addStretch()
        
        setting1 = configCard(title="Welcomer", subtitle="Sends a welcome message")
        setting1.button.checkedChanged.connect(lambda checked: print(checked))
        self.layout.addWidget(setting1)

        setting2 = configCard(title="AI Chat", subtitle="Chat with AI")
        setting2.button.checkedChanged.connect(lambda checked: print(checked))
        self.layout.addWidget(setting2)

        setting3 = configCard(title="Virtual Currency", subtitle="Add a virtual currency")
        setting3.button.checkedChanged.connect(lambda checked: print(checked))
        self.layout.addWidget(setting3)

    def setbotname(self, bot_name):
        self.pagetitle.setText(f"Editing Bot : {bot_name}")