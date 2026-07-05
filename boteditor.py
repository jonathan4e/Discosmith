from PySide6.QtWidgets import QFrame, QVBoxLayout, QStackedWidget, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
import os
import sys
from qfluentwidgets import LineEdit,Flyout, PushButton, DropDownPushButton, SingleDirectionScrollArea, InfoBarIcon, FlyoutAnimationType,  FlyoutView, MessageBox, FluentIcon as FIF, PrimaryDropDownToolButton, RoundMenu, TitleLabel, Action, SwitchButton, CardWidget, BodyLabel, CaptionLabel, TransparentToolButton, PrimaryPushButton
import json
from dotenv import load_dotenv, find_dotenv, set_key
import webbrowser



class newbot(MessageBox):
    def __init__(self, parent=None):
        super().__init__("Add Bot", "Enter bot ClientID:", parent)
        self.name = LineEdit(self)
        self.name.setPlaceholderText("clientid")
        self.name.setClearButtonEnabled(True)
        self.textLayout.addWidget(self.name)
        self.widget.setMinimumWidth(400)

class configCard(CardWidget):
    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent)
        self.title = BodyLabel(title, self)
        self.subtitle = CaptionLabel(subtitle, self)
        self.button = SwitchButton(self)
        #self.more = TransparentToolButton(FIF.MORE, self)
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
        #self.hlayout.addWidget(self.more,0, Qt.AlignRight)
        #self.more.setFixedSize(32,32)



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


        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.setSpacing(10)
        button_layout.addStretch(1)


        self.compilebutton = PrimaryPushButton(FIF.SYNC, "Compile")
        self.compilebutton.setFixedWidth(120)
        self.compilebutton.clicked.connect(self.compile)
        button_layout.addWidget(self.compilebutton, alignment=Qt.AlignRight)

        self.deploybutton = DropDownPushButton(FIF.TILES, "Deploy")
        self.deploybutton.setFixedWidth(120)

        menu = RoundMenu(parent=self.deploybutton)
        menu.addAction(Action(FIF.ADD, "Deploy on JustRunMy.App", self, triggered=lambda: webbrowser.open("https://justrunmy.app/discord-bots")))
        menu.addAction(Action(FIF.ADD, "Deploy on WispByte", self, triggered=lambda: webbrowser.open("https://wispbyte.com/client")))
        menu.addAction(Action(FIF.ADD, "Deploy on fps.me", self, triggered=lambda: webbrowser.open("https://fps.ms/free-discord-bot-hosting/")))
        menu.addAction(Action(FIF.ADD, "Deploy on Replit", self, triggered=lambda: webbrowser.open("https://replit.com/")))
        menu.addAction(Action(FIF.ADD, "Deploy on Railway", self, triggered=lambda: webbrowser.open("https://railway.app/")))
        menu.addAction(Action(FIF.ADD, "Deploy on Render", self, triggered=lambda: webbrowser.open("https://render.com/")))

        menu.addSeparator()
        menu.addAction(Action(FIF.ADD, "Deploy locally", self, triggered=lambda: self.localdeploy()))

        self.deploybutton.setMenu(menu)
        button_layout.addWidget(self.deploybutton, alignment=Qt.AlignRight)

        
        self.addbotbutton = PushButton(FIF.SHARE, "Invite Bot", self)
        self.addbotbutton.setFixedWidth(120)
        self.addbotbutton.clicked.connect(lambda: self.dialogbit())
        button_layout.addWidget(self.addbotbutton, alignment=Qt.AlignRight)
        self.layout.addLayout(button_layout)



        self.scrollarea = SingleDirectionScrollArea(orient=Qt.Vertical, parent=self)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setFrameShape(QFrame.NoFrame)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollarea.setStyleSheet("QScrollArea{background: transparent; border: none}")

        self.scrollwidget = QWidget()
        self.scrollwidget.setStyleSheet("QWidget{background: transparent}")
        self.scrolllayout = QVBoxLayout(self.scrollwidget)
        self.scrolllayout.setContentsMargins(0,10,0,10)
        self.scrolllayout.setSpacing(12)



        self.setting1 = configCard(title="Welcomer", subtitle="Sends a welcome message")
        self.setting1.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile,"WELCOMER","TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting1)

        self.setting2 = configCard(title="AI Chat", subtitle="Chat with AI")
        self.setting2.button.checkedChanged.connect(lambda checked: self.aichat(checked))
        self.scrolllayout.addWidget(self.setting2)

        self.setting3 = configCard(title="Giveaway", subtitle="Start custom giveaways")
        self.setting3.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile,"GA","TRUE" if checked else "FALSE",quote_mode="never"))
        self.scrolllayout.addWidget(self.setting3)

        self.setting4 = configCard(title="Mod Commands", subtitle="Admin Mod Commands")
        self.setting4.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile,"MOD","TRUE"if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting4)

        self.setting5 = configCard(title="Music", subtitle="Stream music in the VC")
        self.setting5.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile,"MUSIC","TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting5)

        self.setting6 = configCard(title="Joke", subtitle="Tell a joke")
        self.setting6.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile, "JOKE", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting6)

        self.setting7 = configCard(title="RPS Game", subtitle="Play Rock Paper Scissors")
        self.setting7.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile, "RPS", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting7)

        self.setting8 = configCard(title="Quote", subtitle="Get a random quote")
        self.setting8.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile, "QUOTE", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting8)

        self.setting9 = configCard(title="Reminder", subtitle="Set a reminder")
        self.setting9.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile, "REMINDER", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting9)

        self.setting10 = configCard(title="Coin flip", subtitle="Flip a coin")
        self.setting10.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile, "COIN", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting10)

        self.setting11 = configCard(title="Server Info", subtitle="Get server information")
        self.setting11.button.checkedChanged.connect(lambda checked:  set_key(self.dotenvfile, "SERVERINFO", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting11)

        self.setting12 = configCard(title="User Info", subtitle="Get user information")
        self.setting12.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile, "USERINFO", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting12)

        self.setting13 = configCard(title="Meme", subtitle="Get a random meme")
        self.setting13.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile, "MEME", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting13)

        self.setting14 = configCard(title="Dice Roll", subtitle="Roll a dice")
        self.setting14.button.checkedChanged.connect(lambda checked: set_key(self.dotenvfile, "DICE", "TRUE" if checked else "FALSE", quote_mode="never"))
        self.scrolllayout.addWidget(self.setting14)

        self.scrolllayout.addStretch(1)
        self.scrollarea.setWidget(self.scrollwidget)
        self.layout.addWidget(self.scrollarea)

        self.console = QFrame(self)
        self.console.setStyleSheet("QFrame { background-color: #202020; border-radius: 6px; border: 1px solid #2c2c2c; }")
        self.consolelayout = QVBoxLayout(self.console)
        self.consolelayout.setContentsMargins(10,10,10,10)

        consoleheader = QHBoxLayout()
        self.consoletitle = TitleLabel("Console", self.console)
        self.consoletitle.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.status = CaptionLabel("● Offline", self.console)


    def dialogbit(self):
        dialog = newbot(self)
        if dialog.exec():
            clientID = dialog.name.text().strip()
            if clientID:
                webbrowser.open(f"https://discord.com/oauth2/authorize?client_id={clientID}&scope=bot%20applications.commands&permissions=8")
            else:
                MessageBox(self, "Error", "Please enter a valid ClientID.")


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
        self.setting7.button.blockSignals(True)
        self.setting8.button.blockSignals(True)
        self.setting9.button.blockSignals(True)
        self.setting10.button.blockSignals(True)
        self.setting11.button.blockSignals(True)
        self.setting12.button.blockSignals(True)
        self.setting13.button.blockSignals(True)
        self.setting14.button.blockSignals(True)
        self.setting1.button.setChecked(os.getenv("WELCOMER") == "TRUE")
        self.setting2.button.setChecked(os.getenv("AI") == "TRUE")
        self.setting3.button.setChecked(os.getenv("GA") == "TRUE")
        self.setting4.button.setChecked(os.getenv("MOD") == "TRUE")
        self.setting5.button.setChecked(os.getenv("MUSIC") == "TRUE")
        self.setting6.button.setChecked(os.getenv("JOKE") == "TRUE")
        self.setting7.button.setChecked(os.getenv("RPS") == "TRUE")
        self.setting8.button.setChecked(os.getenv("QUOTE") == "TRUE")
        self.setting9.button.setChecked(os.getenv("REMINDER") == "TRUE")
        self.setting10.button.setChecked(os.getenv("COIN") == "TRUE")
        self.setting11.button.setChecked(os.getenv("SERVERINFO") == "TRUE")
        self.setting12.button.setChecked(os.getenv("USERINFO") == "TRUE")
        self.setting13.button.setChecked(os.getenv("MEME") == "TRUE")
        self.setting14.button.setChecked(os.getenv("DICE") == "TRUE")
        self.setting1.button.blockSignals(False)
        self.setting2.button.blockSignals(False)
        self.setting3.button.blockSignals(False)
        self.setting4.button.blockSignals(False)
        self.setting5.button.blockSignals(False)
        self.setting6.button.blockSignals(False)
        self.setting7.button.blockSignals(False)
        self.setting8.button.blockSignals(False)
        self.setting9.button.blockSignals(False)
        self.setting10.button.blockSignals(False)
        self.setting11.button.blockSignals(False)
        self.setting12.button.blockSignals(False)
        self.setting13.button.blockSignals(False)
        self.setting14.button.blockSignals(False)


    def compile(self):
        
        template = """
import os
import discord
from dotenv import load_dotenv
from google import genai 
from discord.ext import commands
import random


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
        rps = os.getenv("RPS")
        quote = os.getenv("QUOTE")
        reminder = os.getenv("REMINDER")
        coin = os.getenv("COIN")
        serverinfo = os.getenv("SERVERINFO")
        userinfo = os.getenv("USERINFO")
        meme = os.getenv("MEME")
        dice = os.getenv("DICE")


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
    await interaction.followup.send(f"Now playing: {info["title"]} as requested by {interaction.user.mention}")


""")
                
        else:
            pass


        if joke == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
@bot.hybrid_command(name="joke", description="Tell a joke")
async def joke(ctx):
    await ctx.defer()
    data = requests.get("https://official-joke-api.appspot.com/random_joke").json()
    await ctx.send(f"{data["setup"]} - data["punchline"]")

""")
        else:
            pass


        if rps == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
@bot.hybrid_command(name="rps", description="Play Rock Paper Scissors")
@app_commands.choices(choice = [
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors")
])
                        
async def rps(ctx, choice: str):
    user = choice.lower()
    botchoice = random.choice(["rock", "paper", "scissors"])

    if user == botchoice:
        await ctx.send(f"It's a tie! We both chose {user}.")
    elif (user == "rock" and botchoice == "scissors") or (user == "paper" and botchoice == "rock") or (user == "scissors" and botchoice == "paper"):
        await ctx.send(f"You win! You chose {user} and I chose {botchoice}.")
    else:
        await ctx.send(f"You lose! You chose {user} and I chose {botchoice}.")
                  
""")


        else:
            pass
        

        if quote == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
@bot.hybrid_command(name="quote", description="Get a random quote")
async def quote(ctx):
    await ctx.response.defer()
    data = requests.get("https://api.quotable.io/random").json()
    await ctx.send(f'"{data["content"]}" — {data["author"]}')


""")

        else:
            pass


        if reminder == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
@bot.hybrid_command(name="reminder", description="Set a reminder")
async def reminder(ctx, time: int, message: str):
    await ctx.send(f"Reminder set for {time} seconds from now.")
    await asyncio.sleep(time)
    await ctx.send(f"Reminder: {message} ({ctx.author.mention})")

""")
                
        else:
            pass


        if coin == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
                        
@bot.hybrid_command(name="coinflip", description="Flip a coin")
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"{result} wins!")
                                         
""")


        else:
            pass



        if serverinfo == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
                        
@bot.hybrid_command(name="info", description="Get server info")
async def info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.blue())
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="Created on", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
    embed.add_field(name="Boost Count", value=guild.premium_subscription_count, inline=False)
    embed.set_footer(text=f"Requested by {ctx.author}")
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)
    
                        
""")



        else:
            pass

        if userinfo == "TRUE":
            with open ("bot.py", "a") as f:
                f.write("""

@bot.hybrid_command(name="userinfo", description="Get user info")
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    else:
        member = member
    embed = discord.Embed(title=f"{member.name} Info", color=member.color)      
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Username", value=member.name, inline=False)
    embed.add_field(name="Display Name", value=member.display_name, inline=False)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d"), inline=False)

    await ctx.send(content=f"<@{message.author.id}>", embed=embed)
                        
""")
                
        else:
            pass


        if meme == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
import aiohttp           
@bot.hybrid_command(name="meme", description="Get a random meme")          
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://meme-api.com/gimme") as response:
            data = await response.json()
            await ctx.send(data["url"])
                                    
""")
                
        else:
            pass

    
        if dice == "TRUE":
            with open("bot.py", "a") as f:
                f.write("""
@bot.hybrid_command(name="dice", description="Roll a dice")
async def dice(ctx):
    result = random.randint(1,6)
    await ctx.send(f"You rolled a {result}!")                        
             
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

    def localdeploy(self):
        self.compile()
        os.run("pip install -r requirements.txt")
        os.run("python bot.py")


