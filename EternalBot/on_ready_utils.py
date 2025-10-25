import discord
from GlobalUtils.utils import console_log
# from EternalBot.DiscordUI.ui import InfoButtons, LeaderButtons, TicketButtons
from EternalBot.DiscordUI.ui import InfoButtons, TicketButtons
from StaffList.staff_list_utils import get_departments_settings
from Tickets.tickets_utils import tickets_on_restart

async def info_on_ready(settings: dict, FuncBot: discord.Client, hierarchy_file_path: str, hierarchy_file_encoding: str) -> None:
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
    info_view = InfoButtons(get_departments_settings(hierarchy_file_path, hierarchy_file_encoding), hierarchy_file=hierarchy_file_path, hierarchy_encoding=hierarchy_file_encoding)
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
# async def leader_on_ready(settings: dict, FuncBot: discord.Client) -> None:
#     try:
#         main_board_channel = FuncBot.get_channel(int(settings['leader_settings']['channel']['main_board_channel_id']))
#     except Exception as e:
#         console_log(f"Something went wrong while getting the main board channel for leader, please check the config file! Error: {e}", "error")
#         return
#     messages = []
#     async for message in main_board_channel.history(limit=settings['leader_settings']['channel']['main_board_message_limit']):
#         messages.append(message)
#     leader_embed = discord.Embed(title="Leaderboard", description=settings['leader_settings']['channel']['main_board_message'], color=discord.Color.green())
#     leader_embed.set_thumbnail(url=main_board_channel.guild.icon)
#     leader_view = LeaderButtons()
#     if len(messages) == 0:
#         console_log("There are no messages in the channel!", "info")
#         console_log(f"Creating a new message in {main_board_channel}...", "info")
#         await main_board_channel.send(embed=leader_embed, view=leader_view)
#     elif len(messages) == 1:
#         console_log(f"Detected message in {main_board_channel}, identifying it...", "warning")
#         message_in_channel = messages[0]
#         if message_in_channel.author == FuncBot.user:
#             console_log("Message is from the bot, proceding to editing it...", "info")
#             await message_in_channel.edit(embed=leader_embed, view=leader_view)
#             console_log("Message edited!", "info")
#         else:
#             console_log("Message is not from the bot, proceding to deleting it...", "warning")
#             try:
#                 await message_in_channel.delete()
#                 console_log("Message deleted!", "info")
#             except discord.Forbidden:
#                 console_log(f"I don't have permissions to delete messages in {main_board_channel}!", "error")
#                 return
#             except Exception as e:
#                 console_log(f"Something went wrong while deleting the message! Error: {e}", "error")
#                 return
#             await main_board_channel.send(embed=leader_embed, view=leader_view)
#     else:
#         try:
#             console_log(f"Detected messages in {main_board_channel}, deleting {settings['leader_settings']['channel']['main_board_message_limit']} messages...", "warning")
#             await main_board_channel.delete_messages(messages)
#             console_log("Messages deleted!", "info")
#             await main_board_channel.send(embed=leader_embed, view=leader_view)
#         except discord.Forbidden:
#             console_log(f"I don't have permissions to delete messages in {main_board_channel}!", "error")
#             return
async def ticket_on_ready(settings: dict, FuncBot: discord.Client, categories: dict) -> None:
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
    ticket_view = TicketButtons(categories=categories, category_id=int(settings['ticket_settings']['tickets']['category_id']), FuncBot=FuncBot, log_channel_id=int(settings['ticket_settings']['logs']['channel_id']))
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
    await tickets_on_restart(int(settings['ticket_settings']['tickets']['category_id']), FuncBot, categories, int(settings['ticket_settings']['logs']['channel_id']))