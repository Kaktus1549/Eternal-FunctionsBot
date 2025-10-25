from datetime import datetime
import inspect
import json
import os
import re
from os import getenv
from sys import exit
from GlobalUtils.logging import console_log

def get_current_time():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_datetime
def create_config():
    token = getenv("BOT_TOKEN")
    prefix = getenv("BOT_PREFIX")
    sync = getenv("SYNC_ROLE")

    db_address = getenv("DB_ADDRESS")
    db_user = getenv("DATABASE_USER")
    db_password = getenv("DATABASE_PASSWORD")

    VIP_ENABLED = getenv("VIP_ENABLED")
    KONTRIBUTOR = getenv("KONTRIBUTOR")
    DONATOR = getenv("DONATOR")
    SPONZOR = getenv("SPONZOR")

    LEADERBOARD_ENABLED = getenv("LEADERBOARD_ENABLED")
    LEADERBOARD_CHANNEL = getenv("LEADERBOARD_CHANNEL")
    DEFAULT_LEADERBOARD_TEXT = getenv("DEFAULT_LEADERBOARD_TEXT")
    MESSAGE_LIMIT = getenv("MESSAGE_LIMIT")

    INFO_ENABLED = getenv("INFO_ENABLED")
    INFO_CHANNEL = getenv("INFO_CHANNEL")
    INFO_MESSAGE = getenv("INFO_MESSAGE")
    INFO_LIMIT = getenv("INFO_LIMIT")
    INFO_ROLES = getenv("INFO_ROLES").split(", ")

    TICKETS_ENABLED = getenv("TICKETS_ENABLED")
    TICKETS_CHANNEL = getenv("TICKETS_CHANNEL")
    TICKETS_CATEGORY = getenv("TICKETS_CATEGORY")
    TICKETS_MESSAGE = getenv("TICKETS_MESSAGE")
    TICKETS_LOG_CHANNEL = getenv("TICKETS_LOG_CHANNEL")
    TICKETS_LIMIT = getenv("TICKETS_LIMIT")
    TICKETS_ROLES = getenv("TICKETS_ROLES").split(", ")

    config = {
    "discord_settings": {
        "token": token,
        "prefix": prefix,
        "sync": sync
    },
    "database_settings":{
        "db_address": db_address,
        "db_port": 3306,
        "reconnect": True,
        "db_user": db_user,
        "db_password": db_password,
        "db_name": "EternalGaming"
    },
    "vip_settings": {
        "enabled": VIP_ENABLED,
        "remove": "772112186927480832",
        "json": {
            "file": "./config/vips.json"
        },
        "roles": {
            "kontributor": KONTRIBUTOR,
            "donator": DONATOR,
            "sponzor": SPONZOR
        },
        "db":{
            "table": "Vip",
            "rankTable": "GameRank",
            "playerTable": "Player"
        }
    },
    "leader_settings": {
        "channel": {
            "enabled": LEADERBOARD_ENABLED,
            "main_board_channel_id": LEADERBOARD_CHANNEL,
            "main_board_message": DEFAULT_LEADERBOARD_TEXT,
            "main_board_message_limit": int(MESSAGE_LIMIT)
        },
        "db": {
            "table": "PlayerStatistics",
            "playerTable": "Player"
        }
    },
    "info_settings": {
        "bot": {
            "enabled": INFO_ENABLED,
            "embed_channel_id": INFO_CHANNEL,
            "embed_text": INFO_MESSAGE,
            "message_limit": int(INFO_LIMIT),
            "allowed_roles": INFO_ROLES
        },
        "hiearchy": {
            "file": "./config/hiearchy.json",
            "encoding": "utf-8"
            }
        },
        "ticket_settings":{
            "channel":{
                "enabled": TICKETS_ENABLED,
                "ticket_channel_id": TICKETS_CHANNEL,
                "ticket_message": TICKETS_MESSAGE,
                "ticket_message_limit": int(TICKETS_LIMIT),
                "allowed_roles": TICKETS_ROLES
            },
            "tickets":{
                "file": "./config/tickets.json",
                "encoding": "utf-8",
                "category_id": TICKETS_CATEGORY,
                "ticket_table": "discord_tickets"
            },
            "logs":{
                "channel_id":TICKETS_LOG_CHANNEL,
                "message_limit": "None",
                "table": "discord_tickets_logs",
                "enabled": "true"
            }
        }
    }
    if not os.path.exists("./config"):
        os.mkdir("./config")
    with open('./config/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
def open_config() -> dict:
    global settings
    
    try:
        with open("./config/config.json", "r") as config_file:
            config = json.load(config_file)
            settings = config
            return settings
    except FileNotFoundError:
        console_log("Config file not found! Creating one...", "warning")
        create_config()
        console_log("Config file created! Please fill it out and restart the bot.", "warning")
        exit()
    except Exception as e:
        console_log(f"There was an error while opening the config file: {e}", "error")
        exit()
def is_steamid(steamid):
    # Check if steamid is valid by regex
    # 0 = valid, 1 = invalid
    
    pattern = r'^\d+@steam$'
    match = re.match(pattern, steamid)
    if match:
        return 0
    else:
        return 1