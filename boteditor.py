from PySide6.QtWidgets import QFrame, QVBoxLayout, QStackedWidget, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
import os
import sys
from qfluentwidgets import LineEdit,Flyout, InfoBarIcon, FlyoutAnimationType,  FlyoutView, MessageBox, FluentIcon as FIF, PrimaryDropDownToolButton, RoundMenu, TitleLabel, Action, SwitchButton, CardWidget, BodyLabel, CaptionLabel, TransparentToolButton, PrimaryPushButton
import json
from dotenv import load_dotenv, find_dotenv, set_key


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
        self.vlayout.setSpacing(4)
        self.vlayout.setSpacing(0)
        self.vlayout.addWidget(self.title,0, Qt.AlignVCenter)
        self.vlayout.addWidget(self.subtitle,0, Qt.AlignVCenter)
        self.vlayout.setAlignment(Qt.AlignVCenter)
        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addStretch(1)

        self.hlayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hlayout.addWidget(self.more,0, Qt.AlignRight)
        self.more.setFixedSize(32,32)



class apikeymessage(MessageBox):
    def __init__(self, parent=None):
        super().__init__("Gemini API Key", "Enter Gemini API Key:", parent)
        self.name = LineEdit(self)
        self.name.setPlaceholderText("API Key")
        self.name.setClearButtonEnabled(True)
        self.textLayout.addWidget(self.name)
        self.widget.setMinimumWidth(400)

class boteditor(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30,15,30,30)
        self.layout.setSpacing(12)
        self.pagetitle = TitleLabel("Discosmtih - Bot Editor")
        self.layout.addWidget(self.pagetitle)

        self.dotenvfile = ""


        self.setting1 = configCard(title="Welcomer", subtitle="Sends a welcome message")
        self.setting1.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile,"WELCOMER","TRUE" if checked else "FALSE", quote_mode="never"))
        self.layout.addWidget(self.setting1)

        self.setting2 = configCard(title="AI Chat", subtitle="Chat with AI")
        self.setting2.button.checkedChanged.connect(lambda checked: self.aichat(checked))
        self.layout.addWidget(self.setting2)

        self.setting3 = configCard(title="Giveaway", subtitle="Start custom giveaways")
        self.setting3.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile,"GA","TRUE" if checked else "FALSE",quote_mode="never"))
        self.layout.addWidget(self.setting3)

        self.setting4 = configCard(title="Mod Commands", subtitle="Admin Mod Commands")
        self.setting4.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile,"MOD","TRUE"if checked else "FALSE", quote_mode="never"))
        self.layout.addWidget(self.setting4)

        self.setting5 = configCard(title="Music", subtitle="Stream music in the VC")
        self.setting5.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile,"MUSIC","TRUE" if checked else "FALSE", quote_mode="never"))
        self.layout.addWidget(self.setting5)

        self.setting6 = configCard(title="Joke", subtitle="Tell a joke")
        self.setting6.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile, "JOKE", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.layout.addWidget(self.setting6)

        self.compilebutton = PrimaryPushButton(FIF.SYNC, "Compile")
        self.compilebutton.setFixedWidth(120)
        self.compilebutton.clicked.connect(self.compile)
        self.layout.addWidget(self.compilebutton)

        self.layout.addStretch(1)
    

    def aichat(self, checked):
        if checked:
            apiinput = apikeymessage(self)
            if apiinput.exec():
                api_key = apiinput.name.text().strip()
                set_key(self.dotenvfile,"GEMINI_API_KEY",api_key, quote_mode="never")
                set_key(self.dotenvfile,"AI","TRUE", quote_mode="never")
            else:
                from qfluentwidgets import MessageBox
                MessageBox(self, "Error", "Please enter a valid API key.")
                set_key(self.dotenvfile,"AI","FALSE", quote_mode="never")
        if not checked:
            set_key(self.dotenvfile,"AI","FALSE", quote_mode="never")


    def setbotname(self, bot_name):
        
        self.pagetitle.setText(f"Editing Bot : {bot_name}")
        with open("requirements.txt", "w") as f:
            f.write("discord\ngoogle\nyt-dlp")

    def setdir(self, bot_name):
        targetdir = os.path.abspath(os.path.join(os.getcwd(), bot_name))
        os.makedirs(targetdir, exist_ok=True)
        os.chdir(targetdir)
        self.dotenvfile = os.path.join(targetdir, ".env")
        load_dotenv(self.dotenvfile)
        os.chdir(targetdir)
        self.syncbuttons()
    

    def syncbuttons(self):
        load_dotenv(self.dotenvfile)

        self.setting1.button.blockSignals(True)
        self.setting2.button.blockSignals(True)
        self.setting3.button.blockSignals(True)
        self.setting4.button.blockSignals(True)
        self.setting5.button.blockSignals(True)
        self.setting6.button.blockSignals(True)
        self.setting1.button.setChecked(os.getenv("WELCOMER") == "TRUE")
        self.setting2.button.setChecked(os.getenv("AI") == "TRUE")
        self.setting3.button.setChecked(os.getenv("GA") == "TRUE")
        self.setting4.button.setChecked(os.getenv("MOD") == "TRUE")
        self.setting5.button.setChecked(os.getenv("MUSIC") == "TRUE")
        self.setting6.button.setChecked(os.getenv("JOKE") == "TRUE")
        self.setting1.button.blockSignals(False)
        self.setting2.button.blockSignals(False)
        self.setting3.button.blockSignals(False)
        self.setting4.button.blockSignals(False)
        self.setting5.button.blockSignals(False)
        self.setting6.button.blockSignals(False)

    def compile(self):
        template = """
import os
import discord
from dotenv import load_dotenv
from google import genai 
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is conntected")

    
@bot.tree.command(name= "ping", description = "Check latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong, {latency}ms")

"""
        with open("bot.py", "w") as f:
            f.write(template)
        
        welcome = os.getenv("WELCOMER")
        ai = os.getenv("AI")
        ga = os.getenv("GA")
        mod = os.getenv("MOD")
        music = os.getenv("MUSIC")
        joke = os.getenv("JOKE")

        if welcome == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    channel.send(f"Welcome to the server {member.mention}! :wave:")
                        """)
                
        if ai == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
ai = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))
@bot.tree.command(name="ai", description="Chat with AI")
async def ai(interaction: discord.Interaction):
    await interaction.response.defer()
                        
    response = ai.models.generate_content(model="gemini-3.5-flash", content=prompt)
    await interaction.followup.send(response.text)
                        """)
                
        else:
            pass


        if ga == "TRUE":
            with open("bot.py", "a", encoding="utf-8") as f:
                f.write("""
import asyncio
import random
import time

@bot.tree.command(name="giveaway", description="Start a giveaway")
@discord.app_commands.checks.has_permissions(administrator=True)
async def giveaway(interaction: discord.Interaction, time_days: int, prize: str):
    entries = []
    seconds = time_days * 86400                    
    endtime = int(time.time()) + seconds


    embed = discord.Embed(title="Giveaway for {prize}!", description=f"Ends in <t:{end_time}:R>. Click the button below to enter!", color=0x109319 )
    view = discord.ui.View(timeout=None)
    button = discord.ui.Button(label="Join Giveaway 🎉", style=discord.ButtonStyle.success)

    async def callback(btn_interaction: discord.Interaction):
        if btn_interaction.user.id not in entries:
            entries.append(btn_interaction.user.id)
            await btn_interaction.response.send_message("🎉 You have entered the giveaway!", ephemeral=True)
        else:
            await btn_interaction.response.send_message("You have already entered!", ephemeral=True)

    button.callback = callback
    view.add_item(button)
    await interaction.response.send_message(embed=embed, view=view)
    await asyncio.sleep(seconds)

    button.disabled=True
    button.label = "Giveaway ended"
    button.style = discord.ButtonStyle.secondary

    ga_msg = await interaction.original_response()
    await ga_msg.edit(view=view)

    if entries:
        winner = random.choice(entries)
        await interaction.channel.send(f"🎉 The giveaway has ended! The winner is <@{winner}>! Congrats on winning {prize}!")
    else:
        await interaction.channel.send(f"Giveaway concluded. No one entered the giveaway.")
""")
        else:
            pass

        if mod == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
import datetime

@bot.hybrid_command(name="kick", description="Kick a member from the server")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked from the server. Reason: {reason}")

@bot.hybrid_command(name="ban", description="Ban a member from the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned from the server. Reason: {reason}")

@bot.hybrid_command(name="timeout", description="Timeout a member from the server")
@commands.has_permissions(moderate_member=True)
async def timeout(ctx, member: discord.Member, minutes: int=5, reason="No reason provided"):
    duration=datetime.timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"{member} has been timed out for {minutes} minutes. Reason: {reason}")
                        
@bot.hybrid_command(name="untimout", description="Untimeout a member from the server")
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"{member} has been untimed out.")
                        
@bot.event
async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the required permissions to use this command.")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")


""")
        
        else:
            pass

        if music == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
import yt_dlp

ytdl = yt_dlp.YoutubeDL({"format": "bestaudio/best", "noplaylist": True, "default_search": "ytsearch"})

@bot.tree.command(name="play", description="Play a song in the VC")
async def play(interaction: discord.Interaction, search: str):
    await interaction.response.defer()
    channel = interaction.user.voice.channel
    vc = await channel.connect() if not interaction.guild.voice_client else interaction.guild.voice_client
    info = ytdl.extract_info(search, download = False)
    if "entries" in info:
        info = info["entries"][0]


    url = info["url"]
    vc.play(discord.FFmpegPCMAudio(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn"))
    await interaction.followup.send(f"Now playing: {info["title"]}")


""")
                
        else:
            pass


        if joke == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
@bot.hybrid_command(name="joke", description="Tell a joke")
@async def joke(interaction: discord.Interaction):
    data = requests.get("https://official-joke-api.appspot.com/random_joke").json()
    await interaction.response.send_message(f"{data["setup"]} - data["punchline"]")

""")
        else:
            pass


        with open("bot.py", "a") as f:
            f.write("""
bot.run(TOKEN)
""")
            


        flyout = FlyoutView(icon=InfoBarIcon.SUCCESS, title="Bot Compiled!", content="Your bot has successfully been compiled! Check bot.py for your bot's source code. Make sure to install the required modules from requirements.txt file!", parent=self, isClosable=True)
        w = Flyout.make(flyout, self.compilebutton, self, aniType=FlyoutAnimationType.PULL_UP)
        flyout.closed.connect(w.close)




# joke command to be added soon, along with 
# try expect commands to be added in many places in the code
# deploy button, add bot to server button and send message function to be implemented soon.

