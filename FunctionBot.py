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
        "remove": "772112186927480832"
    },
    "vip_settings":{
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
    for user in data:
        if str(user['DiscordID']) == str(id) or user['UserId'] == str(id) or user['UserId'] == ("!"+str(id)):
            data.remove(user)
            with open(settings['json']['file'], 'w') as json_file:
                json.dump(data, json_file, indent=4)
            return 0
    return 2



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