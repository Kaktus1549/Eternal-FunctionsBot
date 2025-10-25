import discord
from StaffList.staff_list_utils import check_roles


def info_help(ctx: discord.Interaction, bot_avatar: discord.Asset, allowed_roles: list, info_channel_id: int, staff_enabled: bool = False) -> discord.Embed:
    if not staff_enabled:
        return discord.Embed(title="Error", description="Info section is not enabled in the config file!", color=discord.Color.red())
    if not check_roles(ctx.author, allowed_roles):
        help_embed = discord.Embed(title="Help", description="My job is to show the members of each department and section in the server!", color=discord.Color.red())
        help_embed.add_field(name="Info channel", value=f"Channel with the info is here: <#{info_channel_id}>", inline=False)
        try:
            # tryes to get bot avatar
            help_embed.set_thumbnail(url=bot_avatar.url)
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
        help_embed.set_thumbnail(url=bot_avatar.url)
    except:
        # if it fails, sets the default avatar
        help_embed.set_thumbnail(url=ctx.guild.icon)
    help_embed.set_footer(text="Made by Kaktus1549")
    return help_embed
def leader_help(ctx: discord.Interaction, bot_avatar: discord.Asset, statistics_enabled: bool, statistics_channel_id: int) -> discord.Embed:
    if not statistics_enabled:
        return discord.Embed(title="Error", description="Leaderboard section is not enabled in the config file!", color=discord.Color.dark_blue())
    help_embed = discord.Embed(title="Help", description="Here are all commands of the bot", color=discord.Color.dark_blue())
    help_embed.add_field(name=f"**/stats <SteamID/Username>**", value="Shows the stats of the user -> Example: **/stats 76561198119241234@steam** or **/stats Kaktus1549**", inline=False)
    help_embed.add_field(name=f"**/scpleaderboard <PageNumber>**", value="Shows the leaderboard of the server", inline=False)
    main_board_channel = "<#" + str(statistics_channel_id) + ">"
    help_embed.add_field(name="TOP 10 leaderboards", value=f"You can find them in the main board message -> {main_board_channel}", inline=False)
    help_embed.set_footer(text="Made by Kaktus1549")
    try:
        help_embed.set_thumbnail(url=bot_avatar.url)
    except AttributeError:
        help_embed.set_thumbnail(url=ctx.guild.icon)
    return help_embed
def vip_help(ctx: discord.Interaction, bot_avatar: discord.Asset, vip_enabled: bool) -> discord.Embed:
    if not vip_enabled:
        return discord.Embed(title="Error", description="VIP section is not enabled in the config file!", color=discord.Color.green())
    help_embed = discord.Embed(title="VIP bot help", description="Hi, I'm VIP bot! I'm here to activate VIP for users, who have VIP role on discord server!\nWhat are my commands?", color=discord.Color.green())
    help_embed.add_field(name="Vipactivate command", value="**/vipactivate <steamid>** -> Activates VIP on Eternal Gaming if user has VIP role on discord server", inline=False)
    help_embed.add_field(name="Remove command", value="**/remove <steamid | discordid>** -> Admin command, removes vip from user", inline=False)
    help_embed.add_field(name="Help command", value="**/help** -> Shows this message", inline=False)
    try:
        help_embed.set_thumbnail(url=bot_avatar.url)
    except AttributeError:
        help_embed.set_thumbnail(url=ctx.guild.icon)
    help_embed.set_footer(text="Made by Kaktus1549")
    return help_embed
def ticket_help(ctx: discord.Interaction, bot_avatar: discord.Asset, ticket_enabled: bool) -> discord.Embed:
    if not ticket_enabled:
        return discord.Embed(title="Error", description="Ticket section is not enabled in the config file!", color=discord.Color.red())
    help_embed = discord.Embed(title="Help", description="Here are all commands of the bot", color=discord.Color.dark_grey())
    help_embed.add_field(name=f"**/addcategory <CategoryName> <CategoryDescription> <roles>**", value="Adds a category to the ticket system, where roles are roles that are allowed to see the ticket", inline=False)
    help_embed.add_field(name=f"**/updatecategory <CategoryName> <CategoryDescription> <roles>**", value="Updates a category in the ticket system, where roles are roles that are allowed to see the ticket. If roles is empty, it will not be updated", inline=False)
    help_embed.add_field(name=f"**/add_question <CategoryName> <Question> <Placeholder> <style> <mandatory>**", value="Adds a question to the category, where style has to be either text or shorttext, mandatory has to be either true or false", inline=False)
    help_embed.add_field(name=f"**/remove_question <CategoryName> <Question>**", value="Removes a question from the category", inline=False)
    help_embed.add_field(name=f"**/update_question <CategoryName> <Question> <Placeholder> <style> <mandatory>**", value="Updates a question in the category, where style has to be either text or shorttext, mandatory has to be either true or false. If placeholder, style or mandatory is empty, it will not be updated", inline=False)
    help_embed.set_footer(text="Made by Kaktus1549")
    try:
        help_embed.set_thumbnail(url=bot_avatar.url)
    except AttributeError:
        help_embed.set_thumbnail(url=ctx.guild.icon)
    return help_embed