from PySide6.QtWidgets import QFrame, QVBoxLayout, QStackedWidget, QWidget
from PySide6.QtCore import Qt
import os
import sys
from qfluentwidgets import LineEdit, MessageBox, FluentIcon as FIF, PrimaryDropDownToolButton, RoundMenu, TitleLabel, Action
import json

class boteditor(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.title = TitleLabel("Bot Editor")
        self.layout.addWidget(self.title)
        self.layout.addStretch()

    def setbotname(self, bot_name):
        self.title.setText(f"Editing Bot: {bot_name}")