from PySide6.QtWidgets import QFrame, QVBoxLayout, QStackedWidget, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
import os
import sys
from qfluentwidgets import LineEdit, MessageBox, FluentIcon as FIF, PrimaryDropDownToolButton, RoundMenu, TitleLabel, Action, SwitchButton, CardWidget, BodyLabel, CaptionLabel, TransparentToolButton
import json



template = """
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

    
@bot.tree.command(name= "ping", description = "Check latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong, {latency}ms")

bot.run(TOKEN)
"""

file = os.path.join(os.getcwd(), "bot.py")
with open(file, "w") as f:
    file.write(template)



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
        setting1.button.checkedChanged.connect(self.welcomer)
        self.layout.addWidget(setting1)

        setting2 = configCard(title="AI Chat", subtitle="Chat with AI")
        setting2.button.checkedChanged.connect(lambda checked: print(checked))
        self.layout.addWidget(setting2)

        setting3 = configCard(title="Virtual Currency", subtitle="Add a virtual currency")
        setting3.button.checkedChanged.connect(lambda checked: print(checked))
        self.layout.addWidget(setting3)

        setting4 = configCard(title="Mod Commands", subtitle="Admin Mod Commands")
        setting4.button.checkedChanged.connect(lambda checked: print(checked))
        self.layout.addWidget(setting4)

        setting5 = configCard(title="Music", subtitle="Stream music in the VC")
        setting5.button.checkedChanged.connect(lambda checked: print(checked))
        self.layout.addWidget(setting5)
    def setbotname(self, bot_name):
        self.pagetitle.setText(f"Editing Bot : {bot_name}")

    def welcomer(self):
        
        welcome = """
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    channel.send(f"Welcome to the server {member.mention}! :wave:")
"""
        with open(file, "a") as f:
            f.write(welcome)