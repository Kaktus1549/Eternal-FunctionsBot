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
from datetime import datetime, timedelta
from sys import exit
import logging
import os
from os import getenv
from dotenv import load_dotenv
load_dotenv()

# Project libraries
from GlobalUtils.utils import console_log, open_config, create_config
from GlobalUtils.logging import console_log, daily_file_handler
from VIPs.vip_commands import vipactivate, removevip
# from Statistics.statistics_commands import stats, scpleaderboard
from StaffList.staff_list_commands import add_department, remove_department, update_department, add_section, remove_section, update_section, priority as staff_priority
from Tickets.tickets_commands import add_category, remove_category, update_category, add_question, remove_question, update_question
from EternalBot.DiscordUI.ui import HelpButtons
# from EternalBot.on_ready_utils import info_on_ready, leader_on_ready, ticket_on_ready
from EternalBot.on_ready_utils import info_on_ready, ticket_on_ready
from EternalBot.help_utils import info_help, vip_help
# from EternalBot.help_utils import info_help, leader_help, vip_help
from VIPs.vip_utils import load_vips
from Tickets.tickets_utils import load_categories
from Database.db_session import init_db

# Initialize database
print(f"{COLOR_GREEN}Initializing database...{COLOR_RESET}")
try:
    init_db()
    print(f"{COLOR_GREEN}Database initialized successfully!{COLOR_RESET}")
except Exception as e:
    print(f"{COLOR_RED}There was an error while initializing the database: {e}{COLOR_RESET}")
    exit()

# Logging
print(f"{COLOR_GREEN}Setting up logging...{COLOR_RESET}")
if os.path.exists("./logs"):
    file = "./logs/" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".log"
else:
    os.mkdir("./logs")
    file = "./logs/" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".log"

# Checking config
print(f"{COLOR_GREEN}Checking bot config...{COLOR_RESET}")

settings = open_config()

# variables
pool = None
vips = load_vips(settings['vip_settings']['json']['file'])
removers = settings['vip_settings']['remove']
if vips == -1:
    console_log("There was an error while loading VIPs from json file!", "error")
    console_log("Exiting...", "error")
    exit()

ticket_file_path = settings['ticket_settings']['tickets']['file']
categories = load_categories(ticket_file_path)
hierarchy_file_path = settings['info_settings']['hiearchy']['file']
hierarchy_file_encoding = settings['info_settings']['hiearchy']['encoding']
allowed_roles = settings['info_settings']['bot']['allowed_roles']
staff_enabled = settings['info_settings']['bot']['enabled'] == "true"
staff_channel_id = settings['info_settings']['bot']['embed_channel_id']
statistics_enabled = settings['leader_settings']['channel']['enabled'] == "true"
statistics_channel_id = settings['leader_settings']['channel']['main_board_channel_id']
vip_enabled = settings['vip_settings']['enabled'] == "true"

HelpButtons_kwargs = {
    "bot_avatar": None,
    "allowed_roles": allowed_roles,
    "info_channel_id": staff_channel_id,
    "staff_enabled": staff_enabled,
    "statistics_enabled": statistics_enabled,
    "statistics_channel_id": statistics_channel_id,
    "vip_enabled": vip_enabled,
    "ticket_enabled": settings['ticket_settings']['channel']['enabled'] == "true"
}

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
    HelpButtons_kwargs["bot_avatar"] = FuncBot.user.avatar
    if help_type == "info":
        await ctx.send(embed=info_help(ctx, FuncBot.user.avatar, allowed_roles, staff_channel_id, staff_enabled), view=HelpButtons(info_help(ctx, FuncBot.user.avatar, allowed_roles, staff_channel_id, staff_enabled), "info", ctx, **HelpButtons_kwargs))
    # elif help_type == "leader":
    #     await ctx.send(embed=leader_help(ctx, FuncBot.user.avatar, statistics_channel_id, staff_enabled), view=HelpButtons(leader_help(ctx, FuncBot.user.avatar, statistics_channel_id, staff_enabled), "leader", ctx, **HelpButtons_kwargs))
    elif help_type == "vip":
        await ctx.send(embed=vip_help(ctx, FuncBot.user.avatar, vip_enabled), view=HelpButtons(vip_help(ctx, FuncBot.user.avatar, vip_enabled), "vip", ctx, **HelpButtons_kwargs))
    else:
        wrong_help_embed = discord.Embed(title="Error", description="Invalid help type, please use one of these: info, leader, vip", color=discord.Color.red())
        await ctx.send(embed=wrong_help_embed)

@FuncBot.hybrid_command(description="Syncs slash commands with discord")
async def sync(ctx):
    allowed_users = settings['discord_settings']['sync']
    allowed_users = allowed_users.split(",")
    if str(ctx.author.id) in allowed_users:
        await ctx.send("Syncing slash commands with discord...")
        await FuncBot.tree.sync()
        await ctx.send("Sync tree was runned sucessfully!")

# VIP
if settings['vip_settings']['enabled'] == "true":
    @FuncBot.hybrid_command(name="vipactivate", description="Activates VIP on SCP:SL, if user has VIP role on discord server")
    async def bot_vipactivate(ctx, steam_id="-1"):
        try:
            await vipactivate(ctx, steam_id, vips)
        except Exception as e:
            console_log(f"There was an error while activating VIP for user {ctx.author.name}: {e}", "error")
            await ctx.send("There was an error while activating VIP, please try again later.")
    @FuncBot.hybrid_command(name="removevip", description="Removes VIP from user")
    async def bot_removevip(ctx, id="-1"):
        try:
            await removevip(ctx, id, removers)
        except Exception as e:
            console_log(f"There was an error while removing VIP for user {ctx.author.name}: {e}", "error")
            await ctx.send("There was an error while removing VIP, please try again later.")

# # Leaderboard
# if settings['leader_settings']['channel']['enabled'] == "true":
#     @FuncBot.hybrid_command(description="Shows the statistics of user on our server")
#     async def bot_stats(ctx, user="-1"):
#         stats(ctx, user)
#     @FuncBot.hybrid_command(description="Shows the complete leaderboard of our server")
#     async def bot_scpleaderboard(ctx, page=1):
#         scpleaderboard(ctx, page)

# Staff List
if settings['info_settings']['bot']['enabled'] == "true":
    @FuncBot.hybrid_command(description="Sets priority of the department")
    async def bot_priority(ctx, department="-1", priority="-1"):
        await staff_priority(ctx, department, priority, hierarchy_file_path, hierarchy_file_encoding)
    @FuncBot.hybrid_command(description="Adds a department")
    async def bot_add_department(ctx, name="-1", color="grey", text="-1", priority="1000"):
        await add_department(ctx, name, color, text, priority, hierarchy_file_path, hierarchy_file_encoding)
    @FuncBot.hybrid_command(description="Removes a department")
    async def bot_remove_department(ctx, name="-1"):
        await remove_department(ctx, name, hierarchy_file_path, hierarchy_file_encoding)
    @FuncBot.hybrid_command(description="Updates a department")
    async def bot_update_department(ctx, name="-1", color="-1", text="-1"):
        await update_department(ctx, name, color, text, hierarchy_file_path, hierarchy_file_encoding)
    @FuncBot.hybrid_command(description="Adds a section")
    async def bot_add_section(ctx, department="-1", name="-1", role="-1"):
        await add_section(ctx, department, name, role, hierarchy_file_path, hierarchy_file_encoding)
    @FuncBot.hybrid_command(description="Removes a section")
    async def bot_remove_section(ctx, department="-1", name="-1"):
        await remove_section(ctx, department, name, hierarchy_file_path, hierarchy_file_encoding)
    @FuncBot.hybrid_command(description="Updates a section")
    async def bot_update_section(ctx, department="-1", name="-1", role="-1"):
        await update_section(ctx, department, name, role, hierarchy_file_path, hierarchy_file_encoding)

# Ticket
if settings['ticket_settings']['channel']['enabled'] == "true":
    @FuncBot.hybrid_command(description="Adds a category for tickets")
    async def bot_add_category(ctx, name="-1", description="-1", roles="-1"):
        await add_category(ctx, name, description, roles)
    @FuncBot.hybrid_command(description="Removes a category for tickets")
    async def bot_remove_category(ctx, name="-1"):
        await remove_category(ctx, name)
    @FuncBot.hybrid_command(description="Updates a category for tickets")
    async def bot_update_category(ctx, name="-1", description="-1", roles="-1"):
        await update_category(ctx, name, description, roles)
    @FuncBot.hybrid_command(description="Adds question to ticket category")
    async def bot_add_question(ctx, category="-1", question="-1", placeholder="-1", style="text", mandatory="false"):
        await add_question(ctx, category, question, placeholder, style, mandatory)
    @FuncBot.hybrid_command(description="Removes question from ticket category")
    async def bot_remove_question(ctx, category="-1", question="-1"):
        await remove_question(ctx, category, question)
    @FuncBot.hybrid_command(description="Updates question from ticket category")
    async def bot_update_question(ctx, category="-1", question="-1", placeholder="-1", style="-1", mandatory="-1"):
        await update_question(ctx, category, question, placeholder, style, mandatory)

# Discord bot events
@FuncBot.event
async def on_ready():
    try:
        if settings['info_settings']['bot']['enabled'] == "true":
            await info_on_ready(settings=settings, FuncBot=FuncBot, hierarchy_file_path=hierarchy_file_path, hierarchy_file_encoding=hierarchy_file_encoding)
        else:
            console_log("Info module is disabled!", "warning")
        # if settings['leader_settings']['channel']['enabled'] == "true":
        #     await leader_on_ready()
        # else:
        #     console_log("Leaderboard module is disabled!", "warning")
        if settings['ticket_settings']['channel']['enabled'] == "true":
            await ticket_on_ready(settings=settings, FuncBot=FuncBot, categories=categories)
        else:
            console_log("Ticket module is disabled!", "warning")
        console_log(f"Logged in as {FuncBot.user.name}!", "info")
        console_log("Bot is ready!", "info")
    except Exception as e:
        console_log(f"There was an error on bot on_ready event: {e}", "error")

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