from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Qt
import os
import sys
from qfluentwidgets import LineEdit, MessageBox, FluentIcon as FIF, PrimaryDropDownToolButton, RoundMenu, TitleLabel, Action
import json

class dashboard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboard")
        self.title = TitleLabel("Dashboard")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.setLayout(self.layout)

        self.welcome = MessageBox("Welcome to Discosmith!", "Discosmith is a FluentUI based Discord bot maker that allows you to create your own discord bots with ease.", self)
        self.welcome.exec()
        