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
import threading
import inspect

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
class DailyFileHandler(logging.FileHandler):
    def __init__(self, directory, mode='a', encoding=None, delay=False):
        self.directory = directory
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        self.current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        self.date_time = datetime.now().strftime("%Y-%m-%d")
        filename = self._get_filename()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        super().__init__(filename, mode, encoding, delay)

    def _get_filename(self):
        return os.path.join(self.directory, f"{self.current_datetime}.log")

    def emit(self, record):
        new_datetime = datetime.now().strftime("%Y-%m-%d")
        if new_datetime != self.date_time:
            self.current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            self.date_time = new_datetime
            filename = self._get_filename()
            self.baseFilename = filename
            self.stream = self._open()
        super().emit(record)


logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
color_formatter = CustomFormatter(datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(color_formatter)
console_handler.setLevel(logging.DEBUG)


file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)-8s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
daily_file_handler = DailyFileHandler(directory='./logs', encoding='utf-16')
daily_file_handler.setLevel(logging.DEBUG)
daily_file_handler.setFormatter(file_formatter)
logger.addHandler(daily_file_handler)
logger.addHandler(console_handler)

discord_logger = logging.getLogger('discord')
discord_logger.addHandler(console_handler)

# Logs that bot is starting
logger.info(f"============> Starting log {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} <============")

# variables
pool = None
vips = None
categories = None


# Functions for bot
def get_current_time():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_datetime
def console_log(message, status):
    frame = inspect.currentframe()
    outer_frame = inspect.getouterframes(frame)
    caller_frame_record = outer_frame[1]
    caller_line_no = caller_frame_record.lineno
    
    if status == "info":
        logger.info(message)
    elif status == "error":
        message += f" at line {caller_line_no}"
        logger.error(message)
    elif status == "warning":
        logger.warning(message)
    else:
        logger.debug(message)
def create_config():
    config = {
    "discord_settings": {
        "token": "TOKEN",
        "prefix": "#",
        "sync": "772112186927480832"
    },
    "database_settings":{
        "db_address": "127.0.0.1",
        "db_port": 3306,
        "pool_size": 20,
        "reconnect": True,
        "db_user": "test",
        "db_password": "test",
        "db_name": "EternalGaming"
    },
    "vip_settings": {
        "remove": "772112186927480832",
        "json": {
            "file": "./config/vips.json"
        },
        "roles": {
            "kontributor": "1151412247155965952",
            "donator": "ROLE_ID",
            "sponzor": "ROLE_ID",
            "booster": "ROLEID",
            "podporovatel": "ROLEID",
            "investor": "ROLEID"
        },
        "db":{
            "table": "Vip",
            "rankTable": "GameRank",
            "playerTable": "Player"
        }
    },
    "leader_settings": {
        "channel": {
            "enabled": "true",
            "main_board_channel_id": "1140700941889310850",
            "main_board_message": "Default text",
            "main_board_message_limit": 150
        },
        "db": {
            "table": "PlayerStatistics",
            "playerTable": "Player"
        }
    },
    "info_settings": {
        "bot": {
            "enabled": "true",
            "embed_channel_id": "976221389734440981",
            "embed_text": "EDIT_THIS",
            "message_limit": 150,
            "allowed_roles": [
                "978277386091102218"
            ]
        },
        "hiearchy": {
            "file": "./config/hiearchy.json",
            "encoding": "utf-8"
            }
        },
        "ticket_settings":{
            "channel":{
                "enabled": "true",
                "ticket_channel_id": "1196426153280413706",
                "ticket_message": "Create a ticket",
                "ticket_message_limit": 150,
                "allowed_roles": [
                    "978277386091102218"
                ]
            },
            "tickets":{
                "file": "./config/tickets.json",
                "encoding": "utf-8",
                "category_id": "1196748950745653338",
                "ticket_table": "discord_tickets"
            },
            "logs":{
                "channel_id":"978276447909199902",
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
def open_config():
    global settings
    
    try:
        with open("./config/config.json", "r") as config_file:
            config = json.load(config_file)
            settings = config
    except FileNotFoundError:
        console_log("Config file not found! Creating one...", "warning")
        create_config()
        console_log("Config file created! Please fill it out and restart the bot.", "warning")
        exit()
    except Exception as e:
        console_log(f"There was an error while opening the config file: {e}", "error")
        exit()
def pool_connection():
    def connect_db():
        global pool

        console_log("Connecting to the database...", "info")
        try:
            pool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                                pool_size = settings['database_settings']['pool_size'],
                                                                pool_reset_session = settings['database_settings']['reconnect'],
                                                                host = settings['database_settings']['db_address'],
                                                                port = settings['database_settings']['db_port'],
                                                                user = settings['database_settings']['db_user'],
                                                                password = settings['database_settings']['db_password'],
                                                                database = settings['database_settings']['db_name'])
            console_log("Connected to the database!", "info")
        except Exception as e:
            console_log(f"There was an error while connecting to the database! Error: {e}", "error")
    db_thread = threading.Thread(target=connect_db)
    db_thread.start()
def is_steamid(steamid):
    # Check if steamid is valid by regex
    # 0 = valid, 1 = invalid
    
    pattern = r'^\d+@steam$'
    match = re.match(pattern, steamid)
    if match:
        return 0
    else:
        return 1

# VIP functions
def load_vips():
    # 1 = error
    global vips
    
    try:
        with open(settings['vip_settings']['json']['file'], 'r') as json_file:
            data = json.load(json_file)
            vips = data
    except json.decoder.JSONDecodeError or FileNotFoundError:
        console_log("JSON file is empty or doesn't exist!", "warning")
        # if json file is empty, make empty list
        data = []
        # save empty list to json file
        with open(settings['vip_settings']['json']['file'], 'w') as json_file:
            json.dump(data, json_file, indent=4)
        vips = data
    except Exception as e:
        console_log("An error has occured while loading vips! Error: " + str(e), "error")
        vips = 1
def user_check(steamid, discord_id, current_vip):    
    # False = user doesn't have VIP or has one more to share
    # 1 = means VIP upgrade
    # 2 = discord user has VIP
    # 3 = steamid has VIP
    # 4 = error
    
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        # removes @steam from steamid
        steamid = steamid[:-6]
        vip = settings['vip_settings']['db']['table']
        rank = settings['vip_settings']['db']['rankTable']
        cursor.execute(f"SELECT {vip}.Rank_ID, {vip}.Player_ID, {vip}.Activated_DiscordID, {rank}.Identifier, (SELECT ID FROM {rank} WHERE Identifier = %s) AS SpecificRank_ID FROM {vip} JOIN {rank} ON {vip}.Rank_ID = {rank}.ID WHERE {vip}.Player_ID = %s OR {vip}.Activated_DiscordID = %s", (current_vip, steamid, discord_id))
        result = cursor.fetchall()
        if connection.is_connected():
            cursor.close()
            connection.close()
        if len(result) == 0:
            return False
        else:
            if str(result[0][1]) == str(steamid):
                return 3
            # Finds if vip role is allowed to be activated 2 times
            number_of_activations = 0
            for i in vips:
                if i == current_vip:
                    number_of_activations = vips[i]['number_of_activations']
                    break
            # If user role is higher than current vip in database return 1
            for i in result:
                if int(i[0]) > int(i[4]) and str(i[1]) == str(steamid):
                    return 1
            # If user can have another vip role, return False
            if len(result) < int(number_of_activations):
                return False
            # If user has vip role on discord, return 1
            elif str(result[0][2]) == str(discord_id):
                return 2
            # If user has vip role on steamid, return 2
            else:
                return False
    except mysql.connector.Error as e:
        console_log(f"Got an database error while checking the user: {e}", "error")
        return 4
    except Exception as e:
        console_log(f"There was an error while checking the user: {e}", "error")
        return 4
def user_add(steamid, discord_id, vip_role):
    # Status -> 0 = OK, 1 = error

    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        steamid = steamid[:-6]
        # Checks if steamid exists in Player table
        cursor.execute(f"SELECT * FROM {settings['vip_settings']['db']['playerTable']} WHERE SteamID = %s", (steamid,))
        result = cursor.fetchall()
        if len(result) == 0:
            # If steamid doesn't exist, add it to Player table
            cursor.execute(f"INSERT INTO {settings['vip_settings']['db']['playerTable']} (SteamID, DiscordID, Username) VALUES (%s, %s, %s)", (steamid, discord_id, None))
            connection.commit()
        vip_db = vips[vip_role]['db_name']
        ScpSpawn = vips[vip_role]['ScpSpawn']
        HumanSpawn = vips[vip_role]['HumanSpawn']
        WaveRespawn = vips[vip_role]['WaveRespawn']
        ExplosiveVest = vips[vip_role]['ExplosiveVest']
        HHG = vips[vip_role]['HHG']
        Jailbird = vips[vip_role]['Jailbird']
        cursor.execute(f"INSERT INTO {settings['vip_settings']['db']['table']} (Player_ID, Activated_DiscordID, Rank_ID, ScpSpawn, HumanSpawn, WaveRespawn, ExplosiveVest, HHG, Jailbird) VALUES (%s, %s, (SELECT ID FROM {settings['vip_settings']['db']['rankTable']} WHERE Identifier = %s), %s, %s, %s, %s, %s, %s)", (steamid, discord_id, vip_db, ScpSpawn, HumanSpawn, WaveRespawn, ExplosiveVest, HHG, Jailbird))
        connection.commit()
        return 0
    except mysql.connector.Error as e:
        console_log(f"Got an database error while adding the user: {e}", "error")
        return 1
    except Exception as e:
        console_log(f"There was an error while adding the user: {e}", "error")
        return 1
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def user_update(steamid, new_vip_role):
    # Status -> 0 = OK, 1 = error

    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        steamid = steamid[:-6]
        vip_db = vips[new_vip_role]['db_name']
        ScpSpawn = vips[new_vip_role]['ScpSpawn']
        HumanSpawn = vips[new_vip_role]['HumanSpawn']
        WaveRespawn = vips[new_vip_role]['WaveRespawn']
        ExplosiveVest = vips[new_vip_role]['ExplosiveVest']
        HHG = vips[new_vip_role]['HHG']
        Jailbird = vips[new_vip_role]['Jailbird']
        cursor.execute(f"UPDATE {settings['vip_settings']['db']['table']} SET Rank_ID = (SELECT ID FROM {settings['vip_settings']['db']['rankTable']} WHERE Identifier = %s), ScpSpawn = %s, HumanSpawn = %s, WaveRespawn = %s, ExplosiveVest = %s, HHG = %s, Jailbird = %s WHERE Player_ID = %s", (vip_db, ScpSpawn, HumanSpawn, WaveRespawn, ExplosiveVest, HHG, Jailbird, steamid))
        connection.commit()
        return 0
    except mysql.connector.Error as e:
        console_log(f"Got an database error while adding the user: {e}", "error")
        return 1
    except Exception as e:
        console_log(f"There was an error while updating the user: {e}", "error")
        return 1
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def user_remove(id):
    # id = steamid or discordid
    # Status -> 0 = OK, 1 = error, 2 = user not found

    try:
        # Checks if discordid or steamid is in vip and if it is, removes it
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {settings['vip_settings']['db']['table']} WHERE Player_ID = %s OR Activated_DiscordID = %s", (id, id))
        result = cursor.fetchall()
        if len(result) == 0:
            return 2
        else:
            if is_steamid(id) == 0:
                # Removes @steam from steamid
                id = id[:-6]
                cursor.execute(f"DELETE FROM {settings['vip_settings']['db']['table']} WHERE Player_ID = %s", (id,))
                connection.commit()
                return 0
            else:
                cursor.execute(f"DELETE FROM {settings['vip_settings']['db']['table']} WHERE Activated_DiscordID = %s", (id,))
                connection.commit()
                return 0
    except mysql.connector.Error as e:
        console_log(f"Got an database error while removing the user: {e}", "error")
        return 1
    except Exception as e:
        console_log(f"There was an error while removing the user: {e}", "error")
        return 1
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Leader functions
def user_stats(user):
    # -1 means that there was an error while connecting to the database
    # -2 means that user is not found in stats

    # Search for user in database
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        if is_steamid(user) == 0:
            # Removes @steam from steamid
            user = user[:-6]
            cursor.execute(f"SELECT * FROM {settings['leader_settings']['db']['playerTable']} WHERE SteamID = %s", (user,))
            result = cursor.fetchall()
            if len(result) == 0:
                return -2, -2, -2, -2, -2, -2
            else:
                username = result[0][2]
                user = result[0][0]
                cursor.execute(f"SELECT * FROM {settings['leader_settings']['db']['table']} WHERE SteamID = %s", (user,))

        else:
            cursor.execute(f"SELECT * FROM {settings['leader_settings']['db']['playerTable']} WHERE Username = %s", (user,))
            result = cursor.fetchall()
            if len(result) == 0:
                return -2, -2, -2, -2, -2, -2
            else:
                username = result[0][2]
                user = result[0][0]
                cursor.execute(f"SELECT * FROM {settings['leader_settings']['db']['table']} WHERE SteamID = %s", (user,))
        result = cursor.fetchall()
        if connection.is_connected():
            cursor.close()
            connection.close()
        if len(result) == 0:
            return -2, -2, -2, -2, -2, -2
        else:
            userID = result[0][0]
            Humanills = result[0][1]
            ScpKills = result[0][2]
            Deaths = result[0][3]
            TotalSeconds = result[0][4]

            return userID, username, Humanills, ScpKills, Deaths, TotalSeconds
    except mysql.connector.Error as e:
        console_log(f"Got an database error while getting the stats: {e}", "error")
        return -1, -1, -1, -1, -1, -1
    except Exception as e:
        console_log(f"There was an error while getting the stats: {e}", "error")
        return -1, -1, -1, -1, -1, -1
def get_stats(type):
    # -1 means that there was an error while connecting to the database
    # -2 means that stats are empty

    # Sorts users by type from highest to lowest, then returns top 10
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT {settings['leader_settings']['db']['playerTable']}.Username, {settings['leader_settings']['db']['table']}.{type} FROM {settings['leader_settings']['db']['table']} INNER JOIN {settings['leader_settings']['db']['playerTable']} ON {settings['leader_settings']['db']['table']}.SteamID = {settings['leader_settings']['db']['playerTable']}.SteamID ORDER BY {settings['leader_settings']['db']['table']}.{type} DESC")
        result = cursor.fetchall()
        if connection.is_connected():
            cursor.close()
            connection.close()
        if len(result) == 0:
            return -2
        else:
            return result[:10]
    # Except raise OperationalError("MySQL Connection not available.")
    except mysql.connector.Error as e:
        console_log(f"Got an database error while getting the stats: {e}", "error")
        return -1
    except Exception as e:
        console_log(f"There was an error while getting the stats: {e}", "error")
        return -1
def all_players_list(index):
    # -1 means that there was an error while connecting to the database
    # -2 means that stats are empty

    # Sorts users by total sum of ScpKills, HumanKills and TotalSeconds from highest to lowest
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT {settings['leader_settings']['db']['playerTable']}.Username, {settings['leader_settings']['db']['table']}.ScpKills, {settings['leader_settings']['db']['table']}.PlayerKills, {settings['leader_settings']['db']['table']}.Deaths , {settings['leader_settings']['db']['table']}.PlayedSeconds FROM {settings['leader_settings']['db']['table']} INNER JOIN {settings['leader_settings']['db']['playerTable']} ON {settings['leader_settings']['db']['table']}.SteamID = {settings['leader_settings']['db']['playerTable']}.SteamID ORDER BY {settings['leader_settings']['db']['table']}.ScpKills + {settings['leader_settings']['db']['table']}.PlayerKills + {settings['leader_settings']['db']['table']}.PlayedSeconds DESC")
        result = cursor.fetchall()
        if connection.is_connected():
            cursor.close()
            connection.close()
        if len(result) == 0:
            return -2
        else:
            return_list = []
            try:    
                for i in range(10):
                    i = i + index
                    return_list.append(result[i])
            finally:
                return return_list
    except mysql.connector.Error as e:
        console_log(f"Got an database error while getting the stats: {e}", "error")
        return -1
    except Exception as e:
        console_log(f"There was an error while getting the stats: {e}", "error")
        return -1
def get_pages():
    # -1 means that there was an error while connecting to the database

    # Open stats and count pages
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {settings['leader_settings']['db']['table']}")
        result = cursor.fetchall()
        if connection.is_connected():
            cursor.close()
            connection.close()
        pages = result[0][0] // 10
        
        return pages
    except mysql.connector.Error as e:
        console_log(f"Got an database error while getting the stats: {e}", "error")
        return -1
    except Exception as e:
        console_log(f"There was an error while getting the stats: {e}", "error")
        return -1

# Info functions
def create_hiearchy():
    path = settings['info_settings']['hiearchy']['file']
    # Checks if folder exists
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    # Creates hiearchy file
    hiearchy = {}
    with open(path, "w", encoding=settings['info_settings']['hiearchy']['encoding']) as hiearchy_file:
        json.dump(hiearchy, hiearchy_file, indent=4)
def open_hiearchy():
    try:
        with open(settings['info_settings']['hiearchy']['file'], "r", encoding=settings['info_settings']['hiearchy']['encoding']) as hiearchy_file:
            return json.load(hiearchy_file)
    except FileNotFoundError:
        if not os.path.exists(settings['info_settings']['hiearchy']['file']):
            console_log("Hiearchy file not found! Creating one...", "warning")
            create_hiearchy()
            console_log("Hiearchy file created! Please fill it out and restart the bot.", "warning")
            exit()
        hiearchy={}
        with open(settings['info_settings']['hiearchy']['file'], "w", encoding=settings['info_settings']['hiearchy']['encoding']) as hiearchy_file:
            json.dump(hiearchy, hiearchy_file, indent=4)
    except Exception as e:
        console_log(f"There was an error while opening the hiearchy file: {e}", "error")
        return -1
def save_hiearchy(hiearchy):
    try:
        with open(settings['info_settings']['hiearchy']['file'], "w", encoding=settings['info_settings']['hiearchy']['encoding']) as hiearchy_file:
            json.dump(hiearchy, hiearchy_file, indent=4)
    except Exception as e:
        console_log(f"There was an error while saving the hiearchy file: {e}", "error")
        return -1
def get_departments_settings():
    try:
        hiearchy = open_hiearchy()
        if hiearchy == -1:
            return -1
        departments_settings = {}
        for department in hiearchy:
            try:
                department_settings = {
                    f"{department}": {
                    "button_color": f"{hiearchy[department]['settings'][0]}",
                    "button_text": f"{hiearchy[department]['settings'][1]}",
                    "button_privilege": f"{hiearchy[department]['settings'][2]}"}
                    }
            except KeyError:
                console_log(f"Department {department} doesn't have settings, using default settings...", "warning")
                department_settings = {
                    f"{department}": {
                    "button_color": "grey",
                    "button_text": f"{department}",
                    "button_privilege": "1000"}
                    }
            departments_settings.update(department_settings)
        return dict(sorted(departments_settings.items(), key=lambda x: int(x[1]['button_privilege'])))
    except Exception as e:
        console_log(f"There was an error while processing the hiearchy file: {e}", "error")
        return -1
def color_from_hierarchy(color, isButton=True):
    if isButton:
        if color == "red":
            color = discord.ButtonStyle.red
        elif color == "green":
            color = discord.ButtonStyle.green
        elif color == "grey":
            color = discord.ButtonStyle.grey
        elif color == "blue":
            color = discord.ButtonStyle.blurple
        else:
            color = discord.ButtonStyle.grey
    else:
        if color == "red":
            color = discord.Color.red()
        elif color == "green":
            color = discord.Color.green()
        elif color == "grey":
            color = discord.Color.greyple()
        elif color == "blue":
            color = discord.Color.blurple()
        else:
            color = discord.Color.greyple()
    return color
def print_subdepartments(button_id, guild):
    hiearchy = open_hiearchy()
    if hiearchy == -1:
        return discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red())
    try:
        department = hiearchy[button_id]
        color = color_from_hierarchy(department['settings'][0], False)
        embed = discord.Embed(title=f"{department['settings'][1]}", description="", color=color)
        for roles in department:
            if roles != "settings":
                members_with_role = guild.get_role(int(department[roles])).members
                description = ""
                for member in members_with_role:
                    description += f"{member.mention}\n"
                embed.add_field(name=f"{roles}", value=description, inline=False)
        return embed
    except Exception as e:
        console_log(f"Ooops, something went wrong! Error: {e}", "error")
        return discord.Embed(title="Error", description="We are having some technical difficulties, please try again later!", color=discord.Color.red())
def check_roles(member):
    user_roles = member.roles
    allowed_roles = settings['info_settings']['bot']['allowed_roles']

    allow = False
    for role in user_roles:
        if str(role.id) in allowed_roles:
            allow = True
            break
    return allow

# Ticket functions
def load_categories():
    # 1 = error
    global categories
    
    try:
        with open(settings['ticket_settings']['tickets']['file'], 'r') as json_file:
            data = json.load(json_file)
            categories = data
    except json.decoder.JSONDecodeError or FileNotFoundError:
        console_log("JSON file is empty or doesn't exist!", "warning")
        # if json file is empty, make empty list
        data = {}
        # save empty list to json file
        with open(settings['ticket_settings']['tickets']['file'], 'w') as json_file:
            json.dump(data, json_file, indent=4)
        categories = data
    except Exception as e:
        console_log("An error has occured while loading tickets! Error: " + str(e), "error")
        categories = 1
def save_categories():
    try:
        with open(settings['ticket_settings']['tickets']['file'], 'w') as json_file:
            json.dump(categories, json_file, indent=4)
    except Exception as e:
        console_log(f"There was an error while saving the tickets! Error: {e}", "error")
        return -1
async def create_ticket(guild, category, user, form_result= None): 
    # Checks if user has opened ticket, if ticket can be created and if there are any categories
    if has_opened_ticket(user.id):
        error_embed = discord.Embed(title="Error", description="You already have an opened ticket!", color=discord.Color.red())
        return error_embed
    ticket_id = save_ticket_to_db(user.id)
    if categories == None:
        error_embed = discord.Embed(title="Error", description="There was an error while creating the ticket! Please contact the administrator!", color=discord.Color.red())
        console_log("There are no categories!", "warrning")
        return error_embed
    if ticket_id == -1:
        error_embed = discord.Embed(title="Error", description="There was an error while creating the ticket! Please try again or contact the administrator!", color=discord.Color.red())
        console_log("Ticket id is -1!", "error")
        return error_embed
    
    try:
        # Creates ticket channel
        ticket_channel = await guild.create_text_channel(f"ticket-{ticket_id}", category=guild.get_channel(int(settings['ticket_settings']['tickets']['category_id'])))
        
        # Sets permissions for everyone who has role in category
        for role in category['allowed_roles']:
            try:
                guild_role = guild.get_role(int(role))
                await ticket_channel.set_permissions(guild_role, read_messages=True, send_messages=False)
            except Exception as e:
                console_log(f"While setting permissions for role {role} in channel {ticket_channel} an error occured! Error: {e}", "error")
                continue
        # Sets permissions for user who created the ticket
        await ticket_channel.set_permissions(user, read_messages=True, send_messages=True)

        # Sets channel description to category name 
        await ticket_channel.edit(topic=f"{category['name']}")
        
        # Ping all roles that are allowed to see the ticket
        allowed_roles = ""
        for role in category['allowed_roles']:
            allowed_roles += f"<@&{role}> "
        await ticket_channel.send(allowed_roles)
        
        # Creates info embed
        info_embed = discord.Embed(title=f"Ticket-{ticket_id}", description=f"Ticket created by {user.mention}", color=discord.Color.green())
        info_embed.add_field(name=category['name'], value=category['description'], inline=True)
        if form_result != None:
            for answer in form_result:
                if form_result[answer] == None or form_result[answer] == "":
                    user_answer = "Empty"
                else:
                    user_answer = form_result[answer]
                info_embed.add_field(name=answer, value=f"```{user_answer}```", inline=False)
        info_embed.set_thumbnail(url=user.avatar.url)
        view = TicketSolvingButtons(ticket_id, category)
        await ticket_channel.send(embed=info_embed, view=view)
        response_embed = discord.Embed(title="Ticket created!", description=f"Ticket created in {ticket_channel.mention}!", color=discord.Color.green())
        ticket_id += 1
        
        # Returns response embed
        return response_embed
    
    except Exception as e:
        console_log(f"There was an error while creating the ticket! Error: {e}", "error")
        error_embed = discord.Embed(title="Error", description="There was an error while creating the ticket! Please contact the administrator!", color=discord.Color.red())
        return error_embed
def has_opened_ticket(user_id):
    # False = user doesn't have opened ticket
    # True = user has opened ticket
    # -1 = error
    
    try:
        # select all from database where discord id is user id and opened is 1
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {settings['ticket_settings']['tickets']['ticket_table']} WHERE Discord_ID = %s AND Opened = 1", (user_id,))
        result = cursor.fetchall()
        if connection.is_connected():
            cursor.close()
            connection.close()
        if len(result) == 0:
            return False
        else:
            return True
    except mysql.connector.Error as e:
        console_log(f"Got an database error while checking if user has opened ticket: {e}", "error")
        return -1
    except Exception as e:
        console_log(f"There was an error while checking if user has opened ticket! Error: {e}", "error")
        return -1
def save_ticket_to_db(user_id):

    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        # Inserts iscord id into database and returns his ticket id (since ticket id is auto increment)
        cursor.execute(f"INSERT INTO {settings['ticket_settings']['tickets']['ticket_table']} (Discord_ID) VALUES (%s)", (user_id,))
        ticket_id = cursor.lastrowid
        connection.commit()
        return ticket_id
    except mysql.connector.Error as e:
        console_log(f"Got an database error while saving the ticket to database: {e}", "error")
        return -1
    except Exception as e:
        console_log(f"There was an error while saving the ticket to database! Error: {e}", "error")
        return -1
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
async def claim_ticket(ticket_id, staff, channel):

    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        # Updates the ticket in database and sets opened to 0 and claimed to user id
        cursor.execute(f"UPDATE {settings['ticket_settings']['tickets']['ticket_table']} SET Claimed_by = %s WHERE Ticket_ID = %s", (staff.id, ticket_id))
        connection.commit()
        # Sets permissions for user who claimed the ticket
        await channel.set_permissions(staff, read_messages=True, send_messages=True)
        # Changes topic to category name and adds claimed by
        topic = channel.topic
        topic += f" | Claimed by: {staff.mention}"
        await channel.edit(topic=topic)
        return True
    except mysql.connector.Error as e:
        console_log(f"Got an database error while claiming the ticket: {e}", "error")
        error_embed = discord.Embed(title="Error", description="There was an error while claiming the ticket! Please try again or contact the administrator!", color=discord.Color.red())
        return error_embed
    except Exception as e:
        console_log(f"There was an error while claiming the ticket! Error: {e}", "error")
        error_embed = discord.Embed(title="Error", description="There was an error while claiming the ticket! Please try again or contact the administrator!", color=discord.Color.red())
        return error_embed
def check_if_allowed_to_claim(category, user_roles):
    # False = user is not allowed
    # True = user is allowed
    # -1 = error
    try:
        for role in user_roles:
            # checks if user has role that is allowed to claim the ticket or if role is admin
            if str(role.id) in category['allowed_roles'] or role.permissions.administrator:
                return True
        return False
    except Exception as e:
        console_log(f"There was an error while checking if user is allowed to create a ticket! Error: {e}", "error")
        return -1
def check_if_allowed_to_delete(interaction_user, claimed_user):
    # False = user is not allowed
    # True = user is allowed
    # -1 = error
    try:
        if interaction_user == claimed_user and claimed_user != False:
            return True
        else:
            roles = interaction_user.roles
            for role in roles:
                if role.permissions.administrator:
                    return True
            return False
    except Exception as e:
        console_log(f"There was an error while checking if user is allowed to delete the ticket! Error: {e}", "error")
        return -1
async def log_ticket(channel, category, ticket_id):
    # log all messages in ticket channel except bot messages
    # returns complete log
    # -1 = error

    try:
        # get all messages in channel
        messages = []
        log = ""
        async for message in channel.history(limit=None):
            messages.append(message)

        # reverse the list
        messages.reverse()

        # get all messages that are not from bot
        form_log = ""
        for message in messages:
            if message.author != FuncBot.user:
                log += f"{message.author}: {message.content}\n"
            # if message is from bot, check if it is embed
            else:
                if len(message.embeds) != 0:
                    # if it is embed, gets all form fields and adds them to log
                    # first field is always category, so it is not added
                    for field in message.embeds[0].fields:
                        # checks if field is not first field
                        if field.name != category['name']:
                            value = field.value
                            # removes ``` from start and end of value
                            value = value[3:-3]
                            form_log += f"{field.name}: {value}\n"
        # tryies to log messages to database
        try:
            connection = pool.get_connection()
            cursor = connection.cursor()
            # sets Transcript and category in database
            cursor.execute(f"INSERT INTO {settings['ticket_settings']['logs']['table']} (Ticket_ID, Transcript, Category) VALUES (%s, %s, %s)", (ticket_id, log, category['name']))
            connection.commit()
        except mysql.connector.Error as e:
            console_log(f"Got an database error while logging the ticket: {e}", "error")
            return -1, -1
        except Exception as e:
            console_log(f"There was an error while logging the ticket! Error: {e}", "error")
            return -1
        # returns complete log
        return log, form_log
    except Exception as e:
        console_log(f"There was an error while logging the ticket! Error: {e}", "error")
        return -1, -1
async def delete_ticket(interaction, ticket_id, staff, channel, category):
    # Updates database, logs ticket and deletes it
    
    # sends embed with info that ticket is being deleted
    embed = discord.Embed(title="Status", description=f"Deleting ticket-{ticket_id}...", color=discord.Color.red())
    message = await interaction.channel.send(embed=embed)

    try:
        # Updates database
        try:
            # Sets opened status to 0 and returns id of user who created the ticket
            connection = pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"UPDATE {settings['ticket_settings']['tickets']['ticket_table']} SET Opened = 0 WHERE Ticket_ID = %s", (ticket_id,))
            connection.commit()
            cursor.execute(f"SELECT Discord_ID FROM {settings['ticket_settings']['tickets']['ticket_table']} WHERE Ticket_ID = %s", (ticket_id,))
            result = cursor.fetchall()
            user = FuncBot.get_user(int(result[0][0]))
        except mysql.connector.Error as e:
            console_log(f"Got an database error while deleting the ticket: {e}", "error")
            error_embed = discord.Embed(title="Error", description="There was an error while deleting the ticket! Please try again or contact the administrator!", color=discord.Color.red())
            await message.edit(embed=error_embed)
            return
        embed = discord.Embed(title="Status", description=f"Ticket-{ticket_id} marked as closed!", color=discord.Color.green())
        await message.edit(embed=embed)

        # Logs ticket
        log, form_log = await log_ticket(channel, category, ticket_id)
        if log == -1:
            error_embed = discord.Embed(title="Error", description="There was an error while deleting the ticket! Please try again or contact the administrator!", color=discord.Color.red())
            await message.edit(embed=error_embed)
            return
        
        # creates embed where will be: who opened ticket, category with description, transcript and in footer who closed the ticket
        log_embed = discord.Embed(title=f"Ticket-{ticket_id}", description=f"Ticket created by {user.mention}", color=discord.Color.green())
        log_embed.add_field(name=category['name'], value=category['description'], inline=True)
        # transcript in ``` syntax, so it will be in code block
        if form_log != "":
            log_embed.add_field(name="Form", value=f"```{form_log}```", inline=False)
        if log != "":
            log_embed.add_field(name="Transcript", value=f"```{log}```", inline=False)
        else:
            log_embed.add_field(name="Transcript", value="No messages were sent in this ticket!", inline=False)
        log_embed.set_thumbnail(url=user.avatar.url)
        # name of staff who closed the ticket, not mention
        if staff == False:
            try:
                log_embed.set_footer(text=f"Ticket closed by {interaction.user.name}")
            except Exception as e:
                log_embed.set_footer(text=f"Can't get name of user who closed the ticket!")
                console_log(f"Can't get name of user who closed the ticket! Error: {e}", "error")
        else:
            log_embed.set_footer(text=f"Ticket closed by {staff.name}")

        # sends embed into log channel, to staff who claimed the ticket and to user who created the ticket
        try:
            await FuncBot.get_channel(int(settings['ticket_settings']['logs']['channel_id'])).send(embed=log_embed)
            await user.send(embed=log_embed)
            if staff != False:
                await staff.send(embed=log_embed)
        except Exception as e:
            console_log(f"There was an error while sending the embed! Error: {e}", "error")
            error_embed = discord.Embed(title="Error", description="There was an error while deleting the ticket! Please try again or contact the administrator!", color=discord.Color.red())
            await message.edit(embed=error_embed)
            return
        
        # deletes ticket channel
        await channel.delete()
        return
    except Exception as e:
        console_log(f"There was an error while deleting the ticket! Error: {e}", "error")
        error_embed = discord.Embed(title="Error", description="There was an error while deleting the ticket! Please try again or contact the administrator!", color=discord.Color.red())
        await message.edit(embed=error_embed)
        return
async def get_first_five_messages(channel):
    # Fetch a larger set of messages
    messages = []
    async for message in channel.history(limit=None):
        messages.append(message)

    # Sort messages by their creation time in ascending order
    messages.reverse()

    # Get the first five messages
    first_five_messages = messages[:5]
    return first_five_messages
async def tickets_on_restart():
    # Checks if there are any opened tickets in category and if there are, it updates embeds, so they have working buttons
    try:
        category = FuncBot.get_channel(int(settings['ticket_settings']['tickets']['category_id']))
    except Exception as e:
        console_log(f"Something went wrong while getting the category! Error: {e}", "error")
        return
    for channel in category.channels:
        try:
            # Gets first 5 messages in channel
            messages = await get_first_five_messages(channel)
            for message in messages:
                if message.author == FuncBot.user and message.embeds:
                    # if embed name is Ticket-{number}
                    if message.embeds[0].title.startswith("Ticket-"):
                        # Updates embed view
                        topic = channel.topic.split(" | ")
                        category = topic[0]
                        claimed = False
                        if len(topic) == 2:
                            claimed = True
                        view = TicketSolvingButtons(int(channel.name[7:]), categories[category], claimed)
                        await message.edit(view=view)
        except Exception as e:
            console_log(f"Something went wrong while getting the message! Error: {e}", "error")
            continue

# On ready
async def info_on_ready():
    try:
        info_channel = FuncBot.get_channel(int(settings['info_settings']['bot']['embed_channel_id']))
    except Exception as e:
        console_log(f"Something went wrong while getting the main board channel for info, please check the config file! Error: {e}", "error")
        return
    messages = []
    async for message in info_channel.history(limit=settings['info_settings']['bot']['message_limit']):
        messages.append(message)
    info_embed = discord.Embed(title="Info", description=settings['info_settings']['bot']['embed_text'], color=discord.Color.green())
    info_embed.set_thumbnail(url=info_channel.guild.icon)
    info_view = InfoButtons(get_departments_settings())
    if len(messages) == 0:
        console_log("There are no messages in the channel!", "info")
        console_log(f"Creating a new message in {info_channel}...", "info")
        await info_channel.send(embed=info_embed, view=info_view)
    elif len(messages) == 1:
        console_log(f"Detected message in {info_channel}, identifying it...", "warning")
        message_in_channel = messages[0]
        if message_in_channel.author == FuncBot.user:
            console_log("Message is from the bot, proceding to editing it...", "info")
            await message_in_channel.edit(embed=info_embed, view=info_view)
            console_log("Message edited!", "info")
        else:
            console_log("Message is not from the bot, proceding to deleting it...", "warning")
            try:
                await message_in_channel.delete()
                console_log("Message deleted!", "info")
            except discord.Forbidden:
                console_log(f"I don't have permissions to delete messages in {info_channel}!", "error")
                return
            except Exception as e:
                console_log(f"Something went wrong while deleting the message! Error: {e}", "error")
                return
            await info_channel.send(embed=info_embed, view=info_view)
    else:
        try:
            console_log(f"Detected messages in {info_channel}, deleting {settings['info_settings']['bot']['message_limit']} messages...", "warning")
            await info_channel.delete_messages(messages)
            console_log("Messages deleted!", "info")
            await info_channel.send(embed=info_embed, view=info_view)
        except discord.Forbidden:
            console_log(f"I don't have permissions to delete messages in {info_channel}!", "error")
            return
async def leader_on_ready():
    try:
        main_board_channel = FuncBot.get_channel(int(settings['leader_settings']['channel']['main_board_channel_id']))
    except Exception as e:
        console_log(f"Something went wrong while getting the main board channel for leader, please check the config file! Error: {e}", "error")
        return
    messages = []
    async for message in main_board_channel.history(limit=settings['leader_settings']['channel']['main_board_message_limit']):
        messages.append(message)
    leader_embed = discord.Embed(title="Leaderboard", description=settings['leader_settings']['channel']['main_board_message'], color=discord.Color.green())
    leader_embed.set_thumbnail(url=main_board_channel.guild.icon)
    leader_view = LeaderButtons()
    if len(messages) == 0:
        console_log("There are no messages in the channel!", "info")
        console_log(f"Creating a new message in {main_board_channel}...", "info")
        await main_board_channel.send(embed=leader_embed, view=leader_view)
    elif len(messages) == 1:
        console_log(f"Detected message in {main_board_channel}, identifying it...", "warning")
        message_in_channel = messages[0]
        if message_in_channel.author == FuncBot.user:
            console_log("Message is from the bot, proceding to editing it...", "info")
            await message_in_channel.edit(embed=leader_embed, view=leader_view)
            console_log("Message edited!", "info")
        else:
            console_log("Message is not from the bot, proceding to deleting it...", "warning")
            try:
                await message_in_channel.delete()
                console_log("Message deleted!", "info")
            except discord.Forbidden:
                console_log(f"I don't have permissions to delete messages in {main_board_channel}!", "error")
                return
            except Exception as e:
                console_log(f"Something went wrong while deleting the message! Error: {e}", "error")
                return
            await main_board_channel.send(embed=leader_embed, view=leader_view)
    else:
        try:
            console_log(f"Detected messages in {main_board_channel}, deleting {settings['leader_settings']['channel']['main_board_message_limit']} messages...", "warning")
            await main_board_channel.delete_messages(messages)
            console_log("Messages deleted!", "info")
            await main_board_channel.send(embed=leader_embed, view=leader_view)
        except discord.Forbidden:
            console_log(f"I don't have permissions to delete messages in {main_board_channel}!", "error")
            return
async def ticket_on_ready():
    try:
        ticket_channel = FuncBot.get_channel(int(settings['ticket_settings']['channel']['ticket_channel_id']))
    except Exception as e:
        console_log(f"Something went wrong while getting the ticket channel, please check the config file! Error: {e}", "error")
        return
    messages = []
    async for message in ticket_channel.history(limit=settings['ticket_settings']['channel']['ticket_message_limit']):
        messages.append(message)
    ticket_embed = discord.Embed(title="Ticket", description=settings['ticket_settings']['channel']['ticket_message'], color=discord.Color.green())
    ticket_embed.set_thumbnail(url=ticket_channel.guild.icon)
    load_categories()
    ticket_view = TicketButtons(categories=categories)
    if len(messages) == 0:
        console_log("There are no messages in the channel!", "info")
        console_log(f"Creating a new message in {ticket_channel}...", "info")
        await ticket_channel.send(embed=ticket_embed, view=ticket_view)
    elif len(messages) == 1:
        console_log(f"Detected message in {ticket_channel}, identifying it...", "warning")
        message_in_channel = messages[0]
        if message_in_channel.author == FuncBot.user:
            console_log("Message is from the bot, proceding to editing it...", "info")
            await message_in_channel.edit(embed=ticket_embed, view=ticket_view)
            console_log("Message edited!", "info")
        else:
            console_log("Message is not from the bot, proceding to deleting it...", "warning")
            try:
                await message_in_channel.delete()
                console_log("Message deleted!", "info")
            except discord.Forbidden:
                console_log(f"I don't have permissions to delete messages in {ticket_channel}!", "error")
                return
            except Exception as e:
                console_log(f"Something went wrong while deleting the message! Error: {e}", "error")
                return
            await ticket_channel.send(embed=ticket_embed, view=ticket_view)
    await tickets_on_restart()
# Help functions
def info_help(ctx):
    if not check_roles(ctx.author):
        help_embed = discord.Embed(title="Help", description="My job is to show the members of each department and section in the server!", color=discord.Color.red())
        help_embed.add_field(name="Info channel", value=f"Channel with the info is here: <#{settings['info_settings']['bot']['embed_channel_id']}>", inline=False)
        try:
            # tryes to get bot avatar
            help_embed.set_thumbnail(url=FuncBot.user.avatar)
        except:
            # if it fails, sets the default avatar
            help_embed.set_thumbnail(url=ctx.guild.icon)
        help_embed.set_footer(text="Made by Kaktus1549")
        return help_embed
    help_embed = discord.Embed(title="Help", description="My job is to show the members of each department and section in the server!", color=discord.Color.green())
    help_embed.add_field(name="priority", value="Sets the priority of a department, the lower the number, the higher the priority.", inline=False)
    help_embed.add_field(name="add_department", value="Adds a department to the hiearchy.", inline=False)
    help_embed.add_field(name="remove_department", value="Removes a department from the hiearchy.", inline=False)
    help_embed.add_field(name="update_department", value="Updates the settings of a department.", inline=False)
    help_embed.add_field(name="add_section", value="Adds a section to a department.", inline=False)
    help_embed.add_field(name="remove_section", value="Removes a section from a department.", inline=False)
    help_embed.add_field(name="update_section", value="Updates the settings of a section.", inline=False)
    help_embed.add_field(name="reload", value="Reloads the config file.", inline=False)
    help_embed.add_field(name="sync", value="Syncs the slash commands with discord.", inline=False)
    try:
        # tryes to get bot avatar
        help_embed.set_thumbnail(url=FuncBot.user.avatar)
    except:
        # if it fails, sets the default avatar
        help_embed.set_thumbnail(url=ctx.guild.icon)
    help_embed.set_footer(text="Made by Kaktus1549")
    return help_embed
def leader_help(ctx):
    help_embed = discord.Embed(title="Help", description="Here are all commands of the bot", color=discord.Color.dark_blue())
    help_embed.add_field(name=f"**/stats <SteamID/Username>**", value="Shows the stats of the user -> Example: **/stats 76561198119241234@steam** or **/stats Kaktus1549**", inline=False)
    help_embed.add_field(name=f"**/scpleaderboard <PageNumber>**", value="Shows the leaderboard of the server", inline=False)
    main_board_channel = "<#" + settings['leader_settings']['channel']['main_board_channel_id'] + ">"
    help_embed.add_field(name="TOP 10 leaderboards", value=f"You can find them in the main board message -> {main_board_channel}", inline=False)
    help_embed.set_footer(text="Made by Kaktus1549")
    try:
        help_embed.set_thumbnail(url=FuncBot.user.avatar.url)
    except AttributeError:
        help_embed.set_thumbnail(url=ctx.guild.icon)
    return help_embed
def vip_help(ctx):
    help_embed = discord.Embed(title="VIP bot help", description="Hi, I'm VIP bot! I'm here to activate VIP for users, who have VIP role on discord server!\nWhat are my commands?", color=discord.Color.green())
    help_embed.add_field(name="Vipactivate command", value="**/vipactivate <steamid>** -> Activates VIP on Eternal Gaming if user has VIP role on discord server", inline=False)
    help_embed.add_field(name="Remove command", value="**/remove <steamid | discordid>** -> Admin command, removes vip from user", inline=False)
    help_embed.add_field(name="Help command", value="**/help** -> Shows this message", inline=False)
    try:
        help_embed.set_thumbnail(url=FuncBot.user.avatar.url)
    except AttributeError:
        help_embed.set_thumbnail(url=ctx.guild.icon)
    help_embed.set_footer(text="Made by Kaktus1549")
    return help_embed
def ticket_help(ctx):
    help_embed = discord.Embed(title="Help", description="Here are all commands of the bot", color=discord.Color.dark_grey())
    help_embed.add_field(name=f"**/addcategory <CategoryName> <CategoryDescription> <roles>**", value="Adds a category to the ticket system, where roles are roles that are allowed to see the ticket", inline=False)
    help_embed.add_field(name=f"**/updatecategory <CategoryName> <CategoryDescription> <roles>**", value="Updates a category in the ticket system, where roles are roles that are allowed to see the ticket. If roles is empty, it will not be updated", inline=False)
    help_embed.add_field(name=f"**/add_question <CategoryName> <Question> <Placeholder> <style> <mandatory>**", value="Adds a question to the category, where style has to be either text or shorttext, mandatory has to be either true or false", inline=False)
    help_embed.add_field(name=f"**/remove_question <CategoryName> <Question>**", value="Removes a question from the category", inline=False)
    help_embed.add_field(name=f"**/update_question <CategoryName> <Question> <Placeholder> <style> <mandatory>**", value="Updates a question in the category, where style has to be either text or shorttext, mandatory has to be either true or false. If placeholder, style or mandatory is empty, it will not be updated", inline=False)
    help_embed.set_footer(text="Made by Kaktus1549")
    try:
        help_embed.set_thumbnail(url=FuncBot.user.avatar.url)
    except AttributeError:
        help_embed.set_thumbnail(url=ctx.guild.icon)
    return help_embed

# Importing libraries

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
    open_config()
except Exception as e:
    console_log(f"There was an error while importing bot config: {e}", "error")
    exit()
console_log("Importing MySQL...", "info")
try:
        import mysql
        import mysql.connector
        from mysql.connector import Error
        from mysql.connector import pooling
except Exception as e:
    console_log(f"There was an error while importing mysql connector: {e}", "error")
    exit()

# discord.ui
class LeaderButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="SCP Kills", style=discord.ButtonStyle.red, custom_id="scp")
    async def scp_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        SCPKills = get_stats("ScpKills")
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
                stats_embed.add_field(name=f"{i+1}. __{SCPKills[i][0]}__", value=f"**SCP Kills:** {SCPKills[i][1]}", inline=False)
            await interaction.response.send_message(embed=stats_embed, ephemeral=True)
            return
    @discord.ui.button(label="Human Kills", style=discord.ButtonStyle.blurple, custom_id="human")
    async def human_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        HumanKills = get_stats("PlayerKills")
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
                stats_embed.add_field(name=f"{i+1}. __{HumanKills[i][0]}__", value=f"**Human Kills:** {HumanKills[i][1]}", inline=False)
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
            stats_embed = discord.Embed(title="Top 10 Deaths", description="Tady je top 10 hráčů s nejvíce deaths", color=discord.Color.dark_gray())
            for i in range(len(Deaths)):
                stats_embed.add_field(name=f"{i+1}. __{Deaths[i][0]}__", value=f"**Deaths:** {Deaths[i][1]}", inline=False)
            await interaction.response.send_message(embed=stats_embed, ephemeral=True)
            return
    @discord.ui.button(label="Time", style=discord.ButtonStyle.green, custom_id="time")
    async def time_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        Time = get_stats("PlayedSeconds")
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
                time_in_seconds = Time[i][1]
                TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
                stats_embed.add_field(name=f"{i+1}. __{Time[i][0]}__", value=f"**Time:** {TotalTime}", inline=False)
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
                time_in_seconds = players_list[i][4]
                TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
                new_embed.add_field(name=f"{i+1+self.listValue}. __{players_list[i][0]}__", value=f"Odehraný čas: {TotalTime} <==> Počet smrtí: {players_list[i][3]}\nPočet zabitých SCP: {players_list[i][1]} <======> Počet zabitých hráčů: {players_list[i][2]}", inline=False)
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
                time_in_seconds = players_list[i][4]
                TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
                new_embed.add_field(name=f"{i+1+self.listValue}. __{players_list[i][0]}__", value=f"Odehraný čas: {TotalTime} <==> Počet smrtí: {players_list[i][3]}\nPočet zabitých SCP: {players_list[i][1]} <======> Počet zabitých hráčů: {players_list[i][2]}", inline=False)
            new_embed.set_footer(text=f"Page {self.listValue // 10 + 1}/{get_pages()}")
            await interaction.response.edit_message(embed=new_embed, view=self)
class InfoButtons(discord.ui.View):
    def __init__(self, buttons_config):
        super().__init__(timeout=None)
        if buttons_config == -1:
            return -1
        self.buttons_config = buttons_config

        for button_data in buttons_config: 
            label = buttons_config[button_data]['button_text']
            color = color_from_hierarchy(buttons_config[button_data]['button_color'], True)
            custom_id = button_data
            button = discord.ui.Button(label=label, custom_id=custom_id, style=color)
            button.callback = self.button_callback
            self.add_item(button)
    
    async def button_callback(self, interaction: discord.Interaction):
        button_embed = print_subdepartments(interaction.data['custom_id'], interaction.guild)
        await interaction.response.send_message(embed=button_embed, ephemeral=True)
class HelpButtons(discord.ui.View):
    def __init__(self, messageEmbed, help_type, ctx=None):
        super().__init__(timeout=180)
        self.embed = messageEmbed
        self.help_type = help_type
        self.ctx = ctx
    
    @discord.ui.button(label="❔ Info help", style=discord.ButtonStyle.red)
    async def info_help_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.help_type == "info":
            return
        else:
            await interaction.response.edit_message(embed=info_help(self.ctx), view=HelpButtons(info_help(self.ctx), "info", self.ctx))
    @discord.ui.button(label="📊 LeaderBoard help", style=discord.ButtonStyle.blurple)
    async def leader_help_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.help_type == "leader":
            return
        else:
            await interaction.response.edit_message(embed=leader_help(self.ctx), view=HelpButtons(leader_help(self.ctx), "leader", self.ctx))
    @discord.ui.button(label="💶 VIP help", style=discord.ButtonStyle.green)
    async def vip_help_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.help_type == "vip":
            return
        else:
            await interaction.response.edit_message(embed=vip_help(self.ctx), view=HelpButtons(vip_help(self.ctx), "vip", self.ctx))
    @discord.ui.button(label="📩 Ticket help", style=discord.ButtonStyle.gray)
    async def ticket_help_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.help_type == "ticket":
            return
        else:
            await interaction.response.edit_message(embed=ticket_help(self.ctx), view=HelpButtons(ticket_help(self.ctx), "ticket", self.ctx))
class TicketModal(discord.ui.Modal):
    def __init__(self, category, guild, user):
        self.guild = guild
        self.user = user
        self.category = category
        super().__init__(timeout=None, title="Ticket form")
        i = 0
        for question in category['modal_questions']:
            if i >= 5:
                break
            mandatory = category['modal_questions'][question]['mandatory']
            label = category['modal_questions'][question]['label']
            placeholder = category['modal_questions'][question]['placeholder']
            style = category['modal_questions'][question]['style']
            if style == "text":
                style = discord.TextStyle.long
            else:
                style = discord.TextStyle.short
            self.add_item(discord.ui.TextInput(label=label, placeholder=placeholder, style=style, required=mandatory))
    async def on_submit(self, interaction: discord.Interaction):
        form_result = {}
        for item in self.children:
            if isinstance(item, discord.ui.TextInput):
                form_result[item.label] = item.value
        embed = await create_ticket(self.guild, self.category, self.user, form_result)
        await interaction.response.send_message(embed=embed, ephemeral=True)
class TicketDropdown(discord.ui.Select):
    def __init__(self, categories, placeholder, informative=True):
        options = []
        self.informative = informative
        self.categories = categories
        for category in categories:
            options.append(discord.SelectOption(label=category))
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.informative:
            if self.values[0] not in categories:
                error_embed= discord.Embed(title="Error", description="Got mismatched category, please try again!", color=discord.Color.red())
                await interaction.response.edit_message(embed=error_embed)
            else:
                category = self.values[0]
                view = TicketDropdownView(self.categories, category)
                category_embed = discord.Embed(title=f"{category}", description=f"{categories[category]['description']}", color=discord.Color.blurple())
                role_mentions = ""
                for role in categories[category]['allowed_roles']:
                    role_mentions += f"<@&{role}> "
                category_embed.add_field(name="Staff who will handle your ticket:", value=role_mentions, inline=False)
                await interaction.response.edit_message(embed=category_embed, view=view)
        else:
            if self.values[0] not in categories:
                error_embed = discord.Embed(title="Error", description="Got mismatched category, please try again!", color=discord.Color.red())
                await interaction.response.edit_message(embed=error_embed)
            else:
                category = self.values[0]
                modal = TicketModal(categories[category], interaction.guild, interaction.user)
                await interaction.response.send_modal(modal)
class TicketDropdownView(discord.ui.View):
    def __init__(self, categories, placeholder="Select category", informative=True):
        super().__init__(timeout=None)
        if categories == 1 or categories == None:
            self.categories = {}
        self.categories = categories
        dropdown = TicketDropdown(categories, placeholder, informative)
        self.add_item(dropdown)
class TicketButtons(discord.ui.View):
    def __init__(self, categories):
        super().__init__(timeout=None)
        if categories == 1 or categories == None:
            self.categories = {}
        self.categories = categories

    @discord.ui.button(label="📩 Open ticket", style=discord.ButtonStyle.red)
    async def open_ticket_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.categories == {}:
            no_categories = discord.Embed(title="Error", description="I can't find any categories, please contact the administrator!", color=discord.Color.red())
            await interaction.response.send_message(embed=no_categories, ephemeral=True)
            return
        else:
            view = TicketDropdownView(self.categories, informative=False)
            await interaction.response.send_message(embed=discord.Embed(title="Select category", description="Select category from dropdown menu and create ticket!", color=discord.Color.red()), view=view, ephemeral=True)
            return
    
    @discord.ui.button(label="📝 List categories", style=discord.ButtonStyle.blurple)
    async def list_categories_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.categories == {}:
            no_categories = discord.Embed(title="Error", description="I can't find any categories, please contact the administrator!", color=discord.Color.red())
            await interaction.response.send_message(embed=no_categories, ephemeral=True)
            return
        else:
            categories_embed = discord.Embed(title="Categories", description="Select category from dropdown menu and see its description!", color=discord.Color.blurple())
            categories_embed.set_thumbnail(url=interaction.guild.icon)
            view = TicketDropdownView(self.categories)
            await interaction.response.send_message(embed=categories_embed, view=view, ephemeral=True)
class TicketSolvingButtons(discord.ui.View):
    def __init__(self, ticket_id, category, claimed=False):
        super().__init__(timeout=None)
        self.ticket_id = ticket_id
        self.category = category
        self.claimed = claimed
        # Add the "Claim Ticket" button only if the ticket has not been claimed
        if not self.claimed:
            claim_ticket_button = discord.ui.Button(label="🔧 Claim ticket", style=discord.ButtonStyle.green)
            claim_ticket_button.callback = self.claim_ticket_on_click
            self.add_item(claim_ticket_button)
        # Add the "Close Ticket" button
        close_ticket_button = discord.ui.Button(label="🔒 Close ticket", style=discord.ButtonStyle.red)
        close_ticket_button.callback = self.close_ticket_on_click
        self.add_item(close_ticket_button)

    async def claim_ticket_on_click(self, interaction: discord.Interaction):
        allowed = check_if_allowed_to_claim(self.category, interaction.user.roles)
        if allowed:
            await claim_ticket(self.ticket_id, interaction.user, interaction.channel)
            await interaction.response.send_message(embed=discord.Embed(title="Ticket claimed!", description="Ticket has been claimed! You can now solve it now!", color=discord.Color.green()), ephemeral=True)
            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.label == "🔧 Claim ticket":
                    self.remove_item(item)
                    break
            embed = interaction.message.embeds[0]
            embed.add_field(name="Claimed by", value=f"<@{interaction.user.id}>", inline=True)
            await interaction.message.edit(embed=embed, view=self)
            self.claimed = interaction.user
        if not allowed:
            await interaction.response.send_message(embed=discord.Embed(title="Error", description="You are not allowed to claim this ticket!", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Error", description="Something went wrong while claiming the ticket, please contact the administrator!", color=discord.Color.red()), ephemeral=True)
    async def close_ticket_on_click(self, interaction: discord.Interaction):
        allowed = check_if_allowed_to_delete(interaction.user, self.claimed)
        
        if allowed == True:
            await delete_ticket(interaction, self.ticket_id, self.claimed, interaction.channel, self.category)
        if allowed == False:
            await interaction.response.send_message(embed=discord.Embed(title="Error", description="You are not allowed to close this ticket!", color=discord.Color.red()), ephemeral=True)
        if allowed != True and allowed != False and allowed != -1:
            await interaction.response.send_message(embed=discord.Embed(title="Error", description="Something went wrong while closing the ticket, please contact the administrator!", color=discord.Color.red()), ephemeral=True)

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

# Removes default help command
FuncBot.remove_command("help")

# Adds custom help command
@FuncBot.command(name="help")
async def help(ctx, help_type="info"):
    if help_type == "info":
        await ctx.send(embed=info_help(ctx), view=HelpButtons(info_help(ctx), "info", ctx))
    elif help_type == "leader":
        await ctx.send(embed=leader_help(ctx), view=HelpButtons(leader_help(ctx), "leader", ctx))
    elif help_type == "vip":
        await ctx.send(embed=vip_help(ctx), view=HelpButtons(vip_help(ctx), "vip", ctx))
    else:
        wrong_help_embed = discord.Embed(title="Error", description="Invalid help type, please use one of these: info, leader, vip", color=discord.Color.red())
        await ctx.send(embed=wrong_help_embed)

@FuncBot.hybrid_command(description="Syncs slash commands with discord")
async def sync(ctx):
    allowed_roles = settings['discord_settings']['sync']
    allowed_roles = allowed_roles.split(",")
    if str(ctx.author.id) in allowed_roles:
        await ctx.send("Syncing slash commands with discord...")
        await FuncBot.tree.sync()
        await ctx.send("Sync tree was runned sucessfully!")

# VIP
@FuncBot.hybrid_command(name="vipactivate", description="Activates VIP on SCP:SL, if user has VIP role on discord server")
async def vipactivate(ctx, steam_id="-1"):
    steamid = steam_id
    if steamid == "-1" or is_steamid(steamid) == 1:
        invalid_id_embed = discord.Embed(title="Invalid SteamID!", description="Please provide valid SteamID!", color=0xff0000)
        invalid_id_embed.add_field(name="SteamID example", value="12345678901234567@steam", inline=False)
        await ctx.send(embed=invalid_id_embed)
        return
    
    return_message = f"Activating VIP for user **{ctx.author.name}**!"
    return_embed = discord.Embed(title="VIP in progress!", description=return_message, color=discord.Color.dark_grey())
    return_embed.add_field(name="Status", value="Searching for VIP role...", inline=True)
    return_embed = await ctx.send(embed=return_embed)
    console_log(f"{ctx.author.name} has issued command vipactivate", "info")

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
        console_log(f"VIP role found: {vip_status}", "info")

        user_check_embed = discord.Embed(title="VIP in progress!", description=return_message, color=discord.Color.dark_grey())
        user_check_embed.add_field(name="Status", value="Checking if user has VIP activated...", inline=True)
        return_embed = await return_embed.edit(content=None, embed=user_check_embed)

        exists = user_check(steamid, ctx.author.id, vip_status)
        if exists == False:
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
                    await return_embed.edit(content=None, embed=error_vip_embed)
            except Exception as error:
                exception_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
                exception_embed.set_thumbnail(url=ctx.author.avatar.url)
                exception_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
                await return_embed.edit(content=None, embed=exception_embed)
        elif exists == 1:
            update_embed = discord.Embed(title="VIP in progress!", description=return_message, color=discord.Color.dark_grey())
            update_embed.add_field(name="Status", value="Found higher VIP role, updating...", inline=True)
            return_embed = await return_embed.edit(content=None, embed=update_embed)
            try:
                status = user_update(steamid, vip_status)
                if status == 0:
                    console_log(f"VIP for user {ctx.author.name} has been updated!", "info")
                    vip_embed = discord.Embed(title="VIP updated!", description=f"VIP has been updated for user {ctx.author.name}!", color=0x00ff00)
                    vip_embed.set_thumbnail(url=ctx.author.avatar.url)
                    vip_embed.add_field(name="SteamID", value=steamid, inline=True)
                    vip_embed.add_field(name="VIP role", value=vip_status, inline=True)
                    return_embed = await return_embed.edit(content=None ,embed=vip_embed)
                else:
                    error_vip_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
                    error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
                    error_vip_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
                    await return_embed.edit(content=None, embed=error_vip_embed)
            except Exception as error:
                exception_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
                exception_embed.set_thumbnail(url=ctx.author.avatar.url)
                exception_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
                await return_embed.edit(content=None, embed=exception_embed)
        elif exists == 2:
            error_vip_embed = discord.Embed(title="Error!", description=f"Your discord account **{ctx.author.name}** has already VIP activated!", color=0xff0000)
            error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
            await return_embed.edit(content=None, embed=error_vip_embed)
        elif exists == 3:
            error_vip_embed = discord.Embed(title="Error!", description=f"Provided SteamID **{steamid}** has already VIP activated!", color=0xff0000)
            error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
            await return_embed.edit(content=None, embed=error_vip_embed)
        elif exists == 4:
            error_vip_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
            error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
            error_vip_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
            await return_embed.edit(content=None, embed=error_vip_embed)
    else:
        console_log(f"{ctx.author.name} has issued command vipactivate, but doesn't have any VIP role!", "info")
        no_vip_embed = discord.Embed(title="VIP activation failed!", description=return_message, color=0xff0000)
        no_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=no_vip_embed)
@FuncBot.hybrid_command(name="removevip", description="Removes VIP from user")
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

# Leaderboard
@FuncBot.hybrid_command(description="Shows the statistics of user on our server")
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
        user_not_found = discord.Embed(title="Error", description=f"I didn't find any match for **{user}**, maybe you misspelled it? If you are entering steamID, do not forget to add **@steam** at the end!", color=0xff0000)
        await ctx.send(embed=user_not_found)
        return
    total_time = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
    result_embed = discord.Embed(title=f"Steam name: {steam_name}", description=f"SteamID: {steam_id}", color=discord.Color.dark_blue())
    result_embed.add_field(name="Počet zabitých SCP:", value=f"{SCP_kills}", inline=False)
    result_embed.add_field(name="Počet zabitých hráčů:", value=f"{Human_kills}", inline=False)
    result_embed.add_field(name="Počet smrtí:", value=f"{Deaths}", inline=False)
    result_embed.add_field(name="Nahraný čas:", value=f"{total_time}", inline=False)
    await ctx.send(embed=result_embed)
@FuncBot.hybrid_command(description="Shows the complete leaderboard of our server")
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
            time_in_seconds = players_list[i][4]
            TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
            leader_embed.add_field(name=f"{(page - 1) * 10 + i + 1}. __{players_list[i][0]}__", value=f"Odehraný čas: {TotalTime} <==> Počet smrtí: {players_list[i][3]}\nPočet zabitých SCP: {players_list[i][1]} <======> Počet zabitých hráčů: {players_list[i][2]}", inline=False)
        leader_embed.set_footer(text=f"Page {page}/{get_pages()}")
        await ctx.send(embed=leader_embed, view=InteractiveLeaderboard(leader_embed, page))

# Info
@FuncBot.hybrid_command(description="Sets priority of the department")
async def priority(ctx, department="-1", priority="-1"):

    if not check_roles(ctx.author):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if department == "-1" or priority == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the department and the priority!", color=discord.Color.red()))
        return
    if priority is not int and priority.isnumeric() == False:
        await ctx.send(embed=discord.Embed(title="Error", description="Priority needs to be a number!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy()
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        hiearchy[department]['settings'][2] = int(priority)
        save_hiearchy(hiearchy)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Priority of {department} was set to {priority}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while setting the priority: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Adds a department")
async def add_department(ctx, name="-1", color="grey", text="-1", priority="1000"):
    priority = str(priority)
    if not check_roles(ctx.author):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if name == "-1" or text == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the color and the text!", color=discord.Color.red()))
        return
    if priority is not int and priority.isnumeric() == False:
        await ctx.send(embed=discord.Embed(title="Error", description="Priority needs to be a number!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy()
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        hiearchy[name] = {
            "settings": [color, text, priority]
        }
        save_hiearchy(hiearchy)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Department {name} was added!", color=discord.Color.green()))
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while adding the department: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Removes a department")
async def remove_department(ctx, name="-1"):
    if not check_roles(ctx.author):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the name!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy()
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        del hiearchy[name]
        save_hiearchy(hiearchy)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Department {name} was removed!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while removing the department: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Updates a department")
async def update_department(ctx, name="-1", color="-1", text="-1"):
    if not check_roles(ctx.author):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to tell me the name of the department!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy()
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        if color != "-1":
            hiearchy[name]['settings'][0] = color
        if text != "-1":
            hiearchy[name]['settings'][1] = text
        save_hiearchy(hiearchy)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Department {name} was updated!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while updating the department: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Adds a section")
async def add_section(ctx, department="-1", name="-1", role="-1"):
    if not check_roles(ctx.author):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if department == "-1" or name == "-1" or role == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the department, name and role!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy()
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        hiearchy[department][name] = role
        save_hiearchy(hiearchy)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Section {name} was added to {department}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while adding the section: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Removes a section")
async def remove_section(ctx, department="-1", name="-1"):
    if not check_roles(ctx.author):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if department == "-1" or name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the department and the name!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy()
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        del hiearchy[department][name]
        save_hiearchy(hiearchy)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Section {name} was removed from {department}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department or section not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while removing the section: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Updates a section")
async def update_section(ctx, department="-1", name="-1", role="-1"):
    if not check_roles(ctx.author):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if department == "-1" or name == "-1" or role == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the department, name and role!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy()
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        hiearchy[department][name] = role
        save_hiearchy(hiearchy)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Section {name} was updated in {department}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department or section not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while updating the section: {e}", color=discord.Color.red()))
        return  

# Ticket
@FuncBot.hybrid_command(description="Adds a category for tickets")
async def add_category(ctx, name="-1", description="-1", roles="-1"):
    if name == "-1" or description == "-1" or roles == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the name, description and roles!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    try:
        input_roles = roles.split(",")
        roles = []
        for i in range(len(input_roles)):
            if input_roles[i].startswith('<@') and input_roles[i].endswith('>'):
                # Role mention is provided
                roles.append(input_roles[i][3:-1]) # Removing <@& and > from mention
            elif input_roles[i].isnumeric() == False:
                await ctx.send(embed=discord.Embed(title="Error", description="Roles need to be numbers or mentions!", color=discord.Color.red()))
                return
            else:
                roles.append(int(input_roles[i]))
        categories[name] = {
            "description": description,
            "allowed_roles": roles
        }
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Category {name} was added!", color=discord.Color.green()))
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while adding the category: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Removes a category for tickets")
async def remove_category(ctx, name="-1"):
    if name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the name!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    try:
        del categories[name]
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Category {name} was removed!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Category not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while removing the category: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Updates a category for tickets")
async def update_category(ctx, name="-1", description="-1", roles="-1"):
    if name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to specify the name!", color=discord.Color.red()))
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    try:
        if roles != "-1":
            input_roles = input_roles.split(",")
            roles = []
            for i in range(len(input_roles)):
                if input_roles[i].isnumeric() == False:
                    await ctx.send(embed=discord.Embed(title="Error", description="Roles need to be numbers!", color=discord.Color.red()))
                    return
                else:
                    roles.append(int(input_roles[i]))
        else:
            roles = categories[name]['allowed_roles']
        if description == "-1":
            description = categories[name]['description']
        categories[name] = {
            "name": name,
            "description": description,
            "allowed_roles": roles
        }
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Category {name} was updated!", color=discord.Color.green()))
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while updating the category: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Adds question to ticket category")
async def add_question(ctx, category="-1", question="-1", placeholder="-1", style="text", mandatory="false"):
    if category == "-1" or question == "-1" or placeholder == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the category, question, placeholder, style and mandatory!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    allowed_styles = ["text", "shorttext"]
    if style.lower() not in allowed_styles:
        await ctx.send(embed=discord.Embed(title="Error", description=f"Style needs to be one of these: {allowed_styles}", color=discord.Color.red()))
        return
    if mandatory.lower() == "true":
        mandatory = True
    elif mandatory.lower() == "false":
        mandatory = False
    else:
        await ctx.send(embed=discord.Embed(title="Error", description="Mandatory needs to be true or false!", color=discord.Color.red()))
        return
    try:
        categories[category]['modal_questions'][question] = {
            "label": question,
            "placeholder": placeholder,
            "style": style.lower(),
            "mandatory": mandatory
        }
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Question {question} was added to {category}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Category not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while adding the question: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Removes question from ticket category")
async def remove_question(ctx, category="-1", question="-1"):
    if category == "-1" or question == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the category and the question!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    try:
        del categories[category]['modal_questions'][question]
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Question {question} was removed from {category}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Category or question not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while removing the question: {e}", color=discord.Color.red()))
        return
@FuncBot.hybrid_command(description="Updates question from ticket category")
async def update_question(ctx, category="-1", question="-1", placeholder="-1", style="-1", mandatory="-1"):
    if category == "-1" or question == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the category and the question!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    allowed_styles = ["text", "shorttext"]
    if style.lower() not in allowed_styles and style != "-1":
        await ctx.send(embed=discord.Embed(title="Error", description=f"Style needs to be one of these: {allowed_styles}", color=discord.Color.red()))
        return
    if mandatory.lower() == "true":
        mandatory = True
    elif mandatory.lower() == "false":
        mandatory = False
    elif mandatory != "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="Mandatory needs to be true or false!", color=discord.Color.red()))
        return
    try:
        if placeholder != "-1":
            categories[category]['modal_questions'][question]['placeholder'] = placeholder
        if style != "-1":
            categories[category]['modal_questions'][question]['style'] = style.lower()
        if mandatory != "-1":
            categories[category]['modal_questions'][question]['mandatory'] = mandatory
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Question {question} was updated in {category}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Category or question not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while updating the question: {e}", color=discord.Color.red()))
        return

# Discord bot events
@FuncBot.event
async def on_ready():
    pool_connection()
    load_vips()
    if settings['info_settings']['bot']['enabled'] == "true":
        await info_on_ready()
    else:
        console_log("Info module is disabled!", "warning")
    if settings['leader_settings']['channel']['enabled'] == "true":
        await leader_on_ready()
    else:
        console_log("Leaderboard module is disabled!", "warning")
    if settings['ticket_settings']['channel']['enabled'] == "true":
        await ticket_on_ready()
    else:
        console_log("Ticket module is disabled!", "warning")
    console_log(f"Logged in as {FuncBot.user.name}!", "info")
    console_log("Bot is ready!", "info")

# Runs the discord bot
if settings['discord_settings']['token'] == "TOKEN":
    console_log("Discord bot TOKEN not found!", "error")
    exit()
else:
    try:
        console_log("Connecting to discord bot...", "info")
        FuncBot.run(settings['discord_settings']['token'], log_handler=daily_file_handler)
    except Exception as error:
        console_log(f"Discord bot failed to start! Error: {error}", "error")
        console_log("Exiting...", "error")
        exit()

console_log("Discord bot stopped!", "info")
console_log(f"============> Ending log {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} <============", "info")