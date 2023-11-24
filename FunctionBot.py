#colors
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RESET = '\033[0m'
COLOR_BLUE = '\033[94m'
COLOR_GREY = '\033[90m'

print(f"{COLOR_GREEN} ============> Starting Eternal bot! <============{COLOR_RESET}\n")
print(f"{COLOR_GREEN}Importing default libraries...{COLOR_RESET}")

# default libraries
import re
from datetime import datetime, timedelta
from sys import exit
import logging
import os

# Logging
print(f"{COLOR_GREEN}Setting up logging...{COLOR_RESET}")
if os.path.exists("./logs"):
    file = "./logs/" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".log"
else:
    os.mkdir("./logs")
    file = "./logs/" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".log"

class CustomFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        message = record.getMessage()
        
        if levelname == 'DEBUG':
            levelname_color = COLOR_BLUE
            message_color = COLOR_GREEN
        elif levelname == 'INFO':
            levelname_color = COLOR_BLUE
            message_color = COLOR_GREEN
        elif levelname == 'WARNING':
            levelname_color = COLOR_YELLOW
            message_color = COLOR_YELLOW
        elif levelname == 'ERROR':
            levelname_color = COLOR_RED
            message_color = COLOR_RED
        elif levelname == 'CRITICAL':
            levelname_color = COLOR_RED
            message_color = COLOR_RED
        else:
            levelname_color = ''
            message_color = ''
        
        timestamp = self.formatTime(record, self.datefmt)
        levelname_formatted = f'{levelname_color}{levelname:<8}{COLOR_RESET}'
        formatted_message = f'{COLOR_GREY}{timestamp} {levelname_formatted} {message_color}{message}{COLOR_RESET}'
        return formatted_message

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
color_formatter = CustomFormatter(datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(color_formatter)
console_handler.setLevel(logging.DEBUG)


formatter = logging.Formatter('[%(asctime)s] [%(levelname)-8s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(filename=f'{file}', encoding='utf-16', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

discord_logger = logging.getLogger('discord')
discord_logger.addHandler(console_handler)

# Functions for bot
def get_current_time():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_datetime
def console_log(message, status):
    if status == "info":
        logger.info(message)
    elif status == "error":
        logger.error(message)
    elif status == "warning":
        logger.warning(message)
    else:
        logger.debug(message)
def create_config():
    config = {
    "discord_settings":{
        "token": "TOKEN",
        "prefix": "#",
        "sync": "772112186927480832"
    },
    "vip_settings":{
        "remove": "772112186927480832",
        "json":{
            "file": "PATH/TO/VIP.JSON"
        },
        "roles": {
            "kontributor": "ROLE_ID",
            "donator": "ROLE_ID",
            "sponzor": "ROLE_ID",
            "booster": "ROLEID",
            "podporovatel": "ROLEID",
            "investor": "ROLEID"
        }
    },
    "leader_settings":{
        "channel":{
            "main_board_channel_id":"NONE",
            "main_board_message":"Default text",
            "main_board_message_limit":150
        },
        "stats":{
            "stats_file":"PATH/TO/STATS.JSON",
            "encoding": "utf-8"
        }
    },
    "info_settings":{
        "bot":{
            "embed_channel_id":"NONE",
            "embed_text": "EDIT_THIS",
            "message_limit": 150,
            "allowed_roles":[
                "ROLE_ID",
                "ANOTHER_ID"
            ]
        },
        "hiearchy":{
            "file":"PATH/TO/HIEARCHY.JSON",
            "encoding": "utf-8"
        }
    }
    }
    with open('./config/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
def open_config():
    try:
        with open("./config/config.json", "r") as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        console_log("Config file not found! Creating one...", "warning")
        create_config()
        console_log("Config file created! Please fill it out and restart the bot.", "warning")
        exit()
    except Exception as e:
        console_log(f"There was an error while opening the config file: {e}", "error")
        exit()
def load_vips():
    # 1 = error
    # 2 = json file is empty
    
    try:
        with open(settings['vip_settings']['json']['file'], 'r') as json_file:
            data = json.load(json_file)
        return data
    except json.decoder.JSONDecodeError or FileNotFoundError:
        console_log("JSON file is empty or doesn't exist!", "warning")
        # if json file is empty, make empty list
        data = []
        # save empty list to json file
        with open(settings['vip_settings']['json']['file'], 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return 2
    except Exception as e:
        console_log("An error has occured while loading vips! Error: " + str(e), "error")
        return 1
def steamid_validation(steamid):
    # Check if steamid is valid by regex
    
    pattern = r'^\d+@steam$'
    match = re.match(pattern, steamid)
    if match:
        return 0
    else:
        return 1
def user_check(steamid, discord_id):    
    # False = user doesn't have VIP or has one more to share
    # 1 = discord user has VIP
    # 2 = steamid has VIP
    # 3 = error

    # ! before steamid is for david's plugin

    # RoleType:
    # None = 0,
    # Supporter = 1,
    # DiscordBooster = 2,
    # Contributor = 3,
    # Donator = 4,
    # Sponzor = 5
    # Investor = 6
    
    data = load_vips()
    if data == 1:
        return 3
    if data == 2:
        return False
    positive = []
    for user in data:
        if user['UserId'] == steamid or user['UserId'] == ("!"+steamid):
            return 2
        elif str(user['DiscordID']) == str(discord_id):
            if str(user['RoleType']) == "4" or str(user['RoleType']) == "5":
                positive.append(user)
            else:
                return 1
    if len(positive) < 2:
        return False
    else:
        return 1     
def user_add(steamid, discord_id, vip_role):
    # Example: {"UserId":"!<steamID>", "DiscordID":<DiscordID>, "RoleType":<type>, "VipAdvantageData":{"AvailableAdvantages":{}}, "ExpirationDate":<unix timestamp in seconds>}
    # RoleType:
    # None = 0,
    # Supporter = 1,
    # DiscordBooster = 2,
    # Contributor = 3,
    # Donator = 4,
    # Sponzor = 5
    # Investor = 6
    # Status -> 0 = OK, 1 = error

    data = load_vips()
    if data == 1:
        return 1
    # adding user
    steamid = "!" + steamid
    unix_timestamp_in_seconds = int((datetime.now() + timedelta(days=30)).timestamp())
    if vip_role == "podporovatel":
        role_type = 1
    elif vip_role == "booster":
        role_type = 2
    elif vip_role == "kontributor":
        role_type = 3
    elif vip_role == "donator":
        role_type = 4
    elif vip_role == "sponzor":
        role_type = 5
    elif vip_role == "investor":
        role_type = 6
    else:
        # if no match, print error

        console_log(f"Role {vip_role} is unknown!", "error")
        return 1
    user = {"UserId":steamid, "DiscordID":discord_id, "RoleType":role_type, "VipAdvantageData":{"AvailableAdvantages":{}}, "ExpirationDate":unix_timestamp_in_seconds}
    # adding user to json
    data.append(user)
    with open(settings['vip_settings']['json']['file'], 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return 0
def user_remove(id):
    # id = steamid or discordid
    # Status -> 0 = OK, 1 = error, 2 = user not found

    data = load_vips()
    if data == 1:
        return 1
    if data == 2:
        return 2
    for user in data:
        if str(user['DiscordID']) == str(id) or user['UserId'] == str(id) or user['UserId'] == ("!"+str(id)):
            data.remove(user)
            with open(settings['vip_settings']['json']['file'], 'w') as json_file:
                json.dump(data, json_file, indent=4)
            return 0
    return 2
def user_stats(user):
    # -1 means that stats file is not specified in config
    # -2 means that user is not found in stats file
    if settings['leader_settings']['stats']['stats_file'] == "PATH/TO/STATS.JSON":
        console_log("You need to specify the activity json file in the config file!", "error")
        return -1, -1, -1, -1, -1, -1
    # Open json files and return them
    try:
        with open(settings['leader_settings']['stats']['stats_file'], "r", encoding=settings['leader_settings']['stats']['encoding']) as stats_file:
            statistics = json.load(stats_file)
        user_statistics_filter = filter(lambda item: item['UserID'] == user or item['Username'] == user, statistics)
        user_statistics = next(user_statistics_filter, None)
    except FileNotFoundError:
        console_log("Stats file not found, please check the config file!", "error")
        return -1, -1, -1, -1, -1, -1
    if user_statistics == None:
        return -2, -2, -2, -2, -2, -2
    else:
        UserID = user_statistics['UserID']
        Username = user_statistics['Username']
        SCPKills = user_statistics['SCPKills']
        HumanKills = user_statistics['HumanKills']
        Deaths = user_statistics['Deaths']
        TotalSeconds = user_statistics['TotalSeconds']
        return UserID, Username, SCPKills, HumanKills, Deaths, TotalSeconds
def get_stats(type):
    # -1 means that stats file is not specified in config
    # -2 means that stats file is empty
    if settings['leader_settings']['stats']['stats_file'] == "PATH/TO/STATS.JSON":
        console_log("You need to specify the activity json file in the config file!", "error")
        return -1
    # Open json files and return them
    try:
        with open(settings['leader_settings']['stats']['stats_file'], "r", encoding=settings['leader_settings']['stats']['encoding']) as stats_file:
            statistics = json.load(stats_file)
        sorted_statistics = sorted(statistics, key=lambda k: k[type], reverse=True)
    except FileNotFoundError:
        console_log("Stats file not found, please check the config file!", "error")
        return -1, -1, -1, -1, -1, -1
    if sorted_statistics == None:
        return -2
    else:
        top_10 = sorted_statistics[:10]
        return top_10
def all_players_list(index):
    # -1 means that stats file is not specified in config
    # -2 means that stats file is empty
    if settings['leader_settings']['stats']['stats_file'] == "PATH/TO/STATS.JSON":
        console_log("You need to specify the activity json file in the config file!", "error")
        return -1
    # Open json files and return them
    try:
        with open(settings['leader_settings']['stats']['stats_file'], "r", encoding=settings['leader_settings']['stats']['encoding']) as stats_file:
            statistics = json.load(stats_file)
        sorted_statistics = sorted(statistics, key=lambda k: k['TotalScore'], reverse=True)
    except FileNotFoundError:
        console_log("Stats file not found, please check the config file!", "error")
        return -1
    if sorted_statistics == None:
        return -2
    else:
        return_list = []
        try:    
            for i in range(10):
                i = i + index
                return_list.append(sorted_statistics[i])
        finally:
            return return_list       
def get_pages():
    # -1 means that stats file is not specified in config
    if settings['leader_settings']['stats']['stats_file'] == "PATH/TO/STATS.JSON":
        console_log("You need to specify the activity json file in the config file!", "error")
        return -1
    # Open json files and return them
    try:
        with open(settings['leader_settings']['stats']['stats_file'], "r", encoding=settings['leader_settings']['stats']['encoding']) as stats_file:
            statistics = json.load(stats_file)
        pages = len(statistics) // 10
    except FileNotFoundError:
        console_log("Stats file not found, please check the config file!", "error")
        return -1
    if len(statistics) % 10 != 0:
        pages = pages + 1
    return pages



console_log("Importing libraries...", "info")
try:
    import json
except Exception as e:
    console_log(f"There was an error while importing default libraries: {e}", "error")
    exit()
console_log("Importing discord.py...", "info")
try:
    import discord
    from discord.ext import commands, tasks
    from discord.ui import *
except Exception as e:
    console_log(f"There was an error while importing discord.py: {e}", "error")
    exit()
console_log("Importing bot config...", "info")
try:
    settings = open_config()
except Exception as e:
    console_log(f"There was an error while importing bot config: {e}", "error")
    exit()


# discord.ui
class LeaderButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="SCP Kills", style=discord.ButtonStyle.red, custom_id="scp")
    async def scp_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        SCPKills = get_stats("SCPKills")
        if SCPKills == -1:
            error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        elif SCPKills == -2:
            error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        else:
            stats_embed = discord.Embed(title="Top 10 SCP Kills", description="Tady je top 10 hráčů s nejvíce zabitymi SCP", color=0xff0000)
            for i in range(len(SCPKills)):
                stats_embed.add_field(name=f"{i+1}. __{SCPKills[i]['Username']}__", value=f"**SCP Kills:** {SCPKills[i]['SCPKills']}", inline=False)
            await interaction.response.send_message(embed=stats_embed, ephemeral=True)
            return
    @discord.ui.button(label="Human Kills", style=discord.ButtonStyle.blurple, custom_id="human")
    async def human_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        HumanKills = get_stats("HumanKills")
        if HumanKills == -1:
            error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        elif HumanKills == -2:
            error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        else:
            stats_embed = discord.Embed(title="Top 10 Human Kills", description="Tady je top 10 hráčů s nejvíce zabitymi hráči za lidskou roli", color=discord.Color.blurple())
            for i in range(len(HumanKills)):
                stats_embed.add_field(name=f"{i+1}. __{HumanKills[i]['Username']}__", value=f"**Human Kills:** {HumanKills[i]['HumanKills']}", inline=False)
            await interaction.response.send_message(embed=stats_embed, ephemeral=True)
            return
    @discord.ui.button(label="Deaths", style=discord.ButtonStyle.gray, custom_id="deaths")
    async def deaths_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        Deaths = get_stats("Deaths")
        if Deaths == -1:
            error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        elif Deaths == -2:
            error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        else:
            stats_embed = discord.Embed(title="Top 10 Deaths", description="Tady je top 10 hráčů s nejvíce smrtmi", color=discord.Color.dark_gray())
            for i in range(len(Deaths)):
                stats_embed.add_field(name=f"{i+1}. __{Deaths[i]['Username']}__", value=f"**Deaths:** {Deaths[i]['Deaths']}", inline=False)
            await interaction.response.send_message(embed=stats_embed, ephemeral=True)
            return
    @discord.ui.button(label="Time", style=discord.ButtonStyle.green, custom_id="time")
    async def time_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        Time = get_stats("TotalSeconds")
        if Time == -1:
            error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        elif Time == -2:
            error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        else:
            stats_embed = discord.Embed(title="Top 10 Time", description="Tady je top 10 hráčů s nejdelší dobou na serveru", color=discord.Color.green())
            for i in range(len(Time)):
                time_in_seconds = Time[i]['TotalSeconds']
                TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
                stats_embed.add_field(name=f"{i+1}. __{Time[i]['Username']}__", value=f"**Time:** {TotalTime}", inline=False)
            await interaction.response.send_message(embed=stats_embed, ephemeral=True)
            return
class InteractiveLeaderboard(discord.ui.View):
    def __init__(self, messageEmbed, pageNumber=1):
        super().__init__(timeout=600)
        self.listValue = (pageNumber - 1) * 10
        self.embed = messageEmbed
    
    @discord.ui.button(label="⬅️ Previous", style=discord.ButtonStyle.red)
    async def previous_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        self.listValue = self.listValue - 10
        if self.listValue < 0:
            self.listValue = 0
            players_list = all_players_list(self.listValue)
        else:
            players_list = all_players_list(self.listValue)
        if players_list == -1:
            error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        elif players_list == -2:
            error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        else:
            new_embed = discord.Embed(title="All players in one leaderboard", description="Tady jsou všichni hráči na jednom leaderboardu", color=discord.Color.dark_blue())
            new_embed.set_thumbnail(url=interaction.guild.icon)
            for i in range(len(players_list)):
                time_in_seconds = players_list[i]['TotalSeconds']
                TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
                new_embed.add_field(name=f"{i+1+self.listValue}. __{players_list[i]['Username']}__", value=f"Odehraný čas: {TotalTime} <==> Počet smrtí: {players_list[i]['Deaths']}\nPočet zabitých SCP: {players_list[i]['SCPKills']} <======> Počet zabitých hráčů: {players_list[i]['HumanKills']}", inline=False)
            new_embed.set_footer(text=f"Page {self.listValue // 10 + 1}/{get_pages()}")
            await interaction.response.edit_message(embed=new_embed, view=self)
    @discord.ui.button(label="Next ➡️", style=discord.ButtonStyle.red)
    async def next_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        self.listValue = self.listValue + 10
        if (self.listValue // 10) > (get_pages() - 1):
            self.listValue = self.listValue - 10
            players_list = all_players_list(self.listValue)
        else:
            players_list = all_players_list(self.listValue)
        if players_list == -1:
            error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        elif players_list == -2:
            error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
        else:
            new_embed = discord.Embed(title="All players in one leaderboard", description="Tady jsou všichni hráči na jednom leaderboardu", color=discord.Color.dark_blue())
            new_embed.set_thumbnail(url=interaction.guild.icon)
            for i in range(len(players_list)):
                time_in_seconds = players_list[i]['TotalSeconds']
                TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
                new_embed.add_field(name=f"{i+1+self.listValue}. __{players_list[i]['Username']}__", value=f"Odehraný čas: {TotalTime} <==> Počet smrtí: {players_list[i]['Deaths']}\nPočet zabitých SCP: {players_list[i]['SCPKills']} <======> Počet zabitých hráčů: {players_list[i]['HumanKills']}", inline=False)
            new_embed.set_footer(text=f"Page {self.listValue // 10 + 1}/{get_pages()}")
            await interaction.response.edit_message(embed=new_embed, view=self)


# Discord bot settings and intents
try:
    prefix = settings['discord_settings']['prefix']
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    FuncBot = commands.Bot(command_prefix=prefix, intents=intents)
except Exception as e:
    console_log(f"There was an error while inicializing the bot: {e}", "error")
    exit()

# Discord bot commands
@FuncBot.hybrid_command(description="this command can be executed only by owner of bot") # Command will sync slash commands with discord
async def sync(ctx):
    allowed_roles = settings['discord_settings']['sync']
    allowed_roles = allowed_roles.split(",")
    if str(ctx.author.id) in allowed_roles:
        await ctx.send("Syncing slash commands with discord...")
        await FuncBot.tree.sync()
        await ctx.send("Sync tree was runned sucessfully!")
@FuncBot.hybrid_command(name="vipactivate", description="Activates VIP on SCP:SL, if user has VIP role on discord server")
async def vipactivate(ctx, steam_id="-1"):
    steamid = steam_id
    if steamid == "-1" or steamid_validation(steamid) == 1:
        invalid_id_embed = discord.Embed(title="Invalid SteamID!", description="Please provide valid SteamID!", color=0xff0000)
        invalid_id_embed.add_field(name="SteamID example", value="12345678901234567@steam", inline=False)
        await ctx.send(embed=invalid_id_embed)
        return
    exists = user_check(steamid, ctx.author.id)
    if exists == False:
        user_roles = ctx.author.roles
        found_role = False
        for i in settings['vip_settings']['roles']:
            if found_role == True:
                break
            if settings['vip_settings']['roles'][i] == "ROLE_ID":
                console_log(f"Role {i} has not been set in settings.json!", "error")
                return_message = "Disocrd bot has not been configured correctly, please contact bot owner!"
            else:
                for user_role in user_roles:
                    if settings['vip_settings']['roles'][i] == str(user_role.id):
                        vip_status = i
                        found_role = True
                        break
                    else:
                        found_role = False
                        return_message = f"VIP role not found for user **{ctx.author.name}**!"
        if found_role == True:
            return_message = f"Activating VIP for user **{ctx.author.name}**!"
            return_embed = discord.Embed(title="VIP in progress!", description=return_message, color=discord.Color.dark_grey())
            return_embed = await ctx.send(embed=return_embed)
            console_log(f"{ctx.author.name} has issued command vipactivate", "info")
            console_log(f"VIP role: {vip_status}", "info")
            try:
                status = user_add(steamid, ctx.author.id, vip_status)
                if status == 0:
                    console_log(f"VIP for user {ctx.author.name} has been activated!", "info")
                    vip_embed = discord.Embed(title="VIP activated!", description=f"VIP has been activated for user {ctx.author.name}!", color=0x00ff00)
                    vip_embed.set_thumbnail(url=ctx.author.avatar.url)
                    vip_embed.add_field(name="SteamID", value=steamid, inline=True)
                    vip_embed.add_field(name="VIP role", value=vip_status, inline=True)
                    return_embed = await return_embed.edit(content=None ,embed=vip_embed)
                else:
                    error_vip_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
                    error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
                    error_vip_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
                    await ctx.send(embed=error_vip_embed)
            except Exception as error:
                console_log(f"An error has occured while activating VIP for user {ctx.author.name}! Error: {error}", "error")
                await ctx.send(f"An error has occured while activating VIP. Try again later or contact bot owner!")
        else:
            console_log(f"{ctx.author.name} has issued command vipactivate, but doesn't have any VIP role!", "info")
            no_vip_embed = discord.Embed(title="VIP activation failed!", description=return_message, color=0xff0000)
            no_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=no_vip_embed)
    elif exists == 1:
        error_vip_embed = discord.Embed(title="Error!", description=f"Your discord account **{ctx.author.name}** has already VIP activated!", color=0xff0000)
        error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=error_vip_embed)
    elif exists == 2:
        error_vip_embed = discord.Embed(title="Error!", description=f"Provided SteamID **{steamid}** has already VIP activated!", color=0xff0000)
        error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=error_vip_embed)
    elif exists == 3:
        error_vip_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
        error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
        error_vip_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
        await ctx.send(embed=error_vip_embed)
@FuncBot.hybrid_command(name="removevip", description="Only admins can use this command!")
async def removevip(ctx, id="-1"):
    if id == "-1":
        invalid_id_embed = discord.Embed(title="Invalid ID!", description="Please provide valid SteamID or DiscordID!", color=0xff0000)
        await ctx.send(embed=invalid_id_embed)
        return
    allowed_users = settings['vip_settings']['remove'].split(', ')
    for user in allowed_users:
        if user == str(ctx.author.id):
            has_admin = True
            break
        else:
            has_admin = False

    if has_admin == True:
        if id.startswith('<@') and id.endswith('>'):
            # User mention is provided
            user_mention = id
            remove_user_id = user_mention[2:-1] # Removing <@ and > from mention
        else:
            remove_user_id = id
        remove = user_remove(remove_user_id)
        if remove == 0:
            console_log(f"VIP has been removed for id {remove_user_id} by {ctx.author.name}", "info")
            success_embed = discord.Embed(title="Success!", description=f"VIP has been removed for id **{remove_user_id}**!", color=0x00ff00)
            await ctx.send(embed=success_embed)
        elif remove == 2:
            error_embed = discord.Embed(title="Error!", description=f"Provided ID **{remove_user_id}** has no VIP!", color=0xff0000)
            await ctx.send(embed=error_embed)
        elif remove == 1:
            error_embed = discord.Embed(title="Error!", description=f"An error has occured while removing VIP for id **{remove_user_id}**!", color=0xff0000)
            await ctx.send(embed=error_embed)
    else:
        console_log(f"{ctx.author.name} has tried to remove VIP from user {id}, but doesn't have permission!", "info")
        error_embed = discord.Embed(title="Error!", description="You don't have permission to use this command!", color=0xff0000)
        await ctx.send(embed=error_embed)
@FuncBot.hybrid_command(description="Shows the stats of the user")
async def stats(ctx, user="-1"):
    if user == "-1":
        no_argument_embed = discord.Embed(title="Error", description="You need to specify a steamID or steam name", color=0xff0000)
        no_argument_embed.add_field(name="Example", value=f"**65433444@steam** or **Kaktus1549**", inline=False)
        await ctx.send(embed=no_argument_embed)
        return
    steam_id, steam_name, SCP_kills, Human_kills, Deaths, time_in_seconds = user_stats(user)
    if steam_id == -1:
        settings_error = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
        await ctx.send(embed=settings_error)
        return
    elif steam_id == -2:
        user_not_found = discord.Embed(title="Error", description=f"I didn't find any match for **{user}**, maybe you misspelled it?", color=0xff0000)
        await ctx.send(embed=user_not_found)
        return
    total_time = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
    result_embed = discord.Embed(title=f"Steam name: {steam_name}", description=f"SteamID: {steam_id}", color=discord.Color.dark_blue())
    result_embed.add_field(name="Počet zabitých SCP:", value=f"{SCP_kills}", inline=False)
    result_embed.add_field(name="Počet zabitých hráčů:", value=f"{Human_kills}", inline=False)
    result_embed.add_field(name="Počet smrtí:", value=f"{Deaths}", inline=False)
    result_embed.add_field(name="Nahraný čas:", value=f"{total_time}", inline=False)
    await ctx.send(embed=result_embed)
@FuncBot.hybrid_command(description="Shows the leaderboard of the server")
async def scpleaderboard(ctx, page=1):
    if page > get_pages():
        page = get_pages()
    elif page < 1:
        page = 1
    leader_embed = discord.Embed(title="All players in one leaderboard", description="Tady jsou všichni hráči na jednom leaderboardu", color=discord.Color.dark_blue())
    leader_embed.set_thumbnail(url=ctx.guild.icon)
    players_list = all_players_list((page - 1) * 10)
    if players_list == -1:
        settings_error = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
        await ctx.send(embed=settings_error)
        return
    elif players_list == -2:
        user_not_found = discord.Embed(title="Error", description=f"There was something wrong while getting the stats, please contact the administrator", color=0xff0000)
        await ctx.send(embed=user_not_found)
        return
    else:
        for i in range(len(players_list)):
            time_in_seconds = players_list[i]['TotalSeconds']
            TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
            leader_embed.add_field(name=f"{(page - 1) * 10 + i + 1}. __{players_list[i]['Username']}__", value=f"Odehraný čas: {TotalTime} <==> Počet smrtí: {players_list[i]['Deaths']}\nPočet zabitých SCP: {players_list[i]['SCPKills']} <======> Počet zabitých hráčů: {players_list[i]['HumanKills']}", inline=False)
        leader_embed.set_footer(text=f"Page {page}/{get_pages()}")
        await ctx.send(embed=leader_embed, view=InteractiveLeaderboard(leader_embed, page))

# Discord bot events



if settings['discord_settings']['token'] == "TOKEN":
    console_log("Discord bot TOKEN not found!", "error")
    exit()
else:
    try:
        console_log("Connecting to discord bot...", "info")
        FuncBot.run(settings['discord_settings']['token'], log_handler=file_handler)
    except Exception as error:
        console_log(f"Discord bot failed to start! Error: {error}", "error")
        console_log("Exiting...", "error")
        exit()