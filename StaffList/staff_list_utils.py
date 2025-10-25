import os
import json
from GlobalUtils.utils import console_log
import discord
from sys import exit

def create_hiearchy(settings: dict) -> None:
    path = settings['info_settings']['hiearchy']['file']
    # Checks if folder exists
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    # Creates hiearchy file
    hiearchy = {}
    with open(path, "w", encoding=settings['info_settings']['hiearchy']['encoding']) as hiearchy_file:
        json.dump(hiearchy, hiearchy_file, indent=4)
def open_hiearchy(file_path: str, file_encoding: str) -> dict | int:
    try:
        with open(file_path, "r", encoding=file_encoding) as hiearchy_file:
            return json.load(hiearchy_file)
    except FileNotFoundError:
        if not os.path.exists(file_path):
            console_log("Hiearchy file not found! Creating one...", "warning")
            create_hiearchy()
            console_log("Hiearchy file created! Please fill it out and restart the bot.", "warning")
            exit()
        hiearchy={}
        with open(file_path, "w", encoding=file_encoding) as hiearchy_file:
            json.dump(hiearchy, hiearchy_file, indent=4)
        return hiearchy
    except Exception as e:
        console_log(f"There was an error while opening the hiearchy file: {e}", "error")
        return -1
def save_hiearchy(hiearchy: dict, file_path: str, file_encoding: str) -> int:
    try:
        with open(file_path, "w", encoding=file_encoding) as hiearchy_file:
            json.dump(hiearchy, hiearchy_file, indent=4)
    except Exception as e:
        console_log(f"There was an error while saving the hiearchy file: {e}", "error")
        return -1
def get_departments_settings(hiearchy_file_path: str, hiearchy_file_encoding: str) -> dict | int:
    try:
        hiearchy = open_hiearchy(hiearchy_file_path, hiearchy_file_encoding)
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
def color_from_hierarchy(color: str, isButton: bool = True) -> discord.ButtonStyle | discord.Color:
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
def print_subdepartments(button_id: str, guild: discord.Guild, hiearchy_file_path: str, hiearchy_file_encoding: str) -> discord.Embed:
    hiearchy = open_hiearchy(hiearchy_file_path, hiearchy_file_encoding)
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
def check_roles(member: discord.Member, allowed_roles: list) -> bool:
    user_roles = member.roles

    allow = False
    for role in user_roles:
        if str(role.id) in allowed_roles:
            allow = True
            break
    return allow