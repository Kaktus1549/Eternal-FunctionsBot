import discord
import io
import json
from sys import exit
from GlobalUtils.logging import console_log
from EternalBot.DiscordUI.ui import TicketSolvingButtons
from Database.db_session import get_session
from Database.DiscordTicketLog import DiscordTicketLog
from Database.DiscordTicket import DiscordTicket

def load_categories(tickets_file: str) -> dict:
    # -1 = error
    
    try:
        with open(tickets_file, 'r') as json_file:
            data = json.load(json_file)
            categories = data
        return categories
    except json.decoder.JSONDecodeError or FileNotFoundError:
        console_log("JSON file is empty or doesn't exist!", "warning")
        # if json file is empty, make empty list
        data = {}
        # save empty list to json file
        with open(tickets_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        categories = data
        return categories
    except Exception as e:
        console_log("An error has occured while loading tickets! Error: " + str(e), "error")
        exit(-1)
def save_categories(categories: dict, tickets_file: str) -> int:
    try:
        with open(tickets_file, 'w') as json_file:
            json.dump(categories, json_file, indent=4)
    except Exception as e:
        console_log(f"There was an error while saving the tickets! Error: {e}", "error")
        return -1
async def create_ticket(guild: discord.Guild, category: dict, user: discord.User, category_id: int, categories: dict, FuncBot: discord.Client, log_channel_id: int, form_result= None) -> discord.Embed:
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
        ticket_channel = await guild.create_text_channel(f"ticket-{ticket_id}", category=guild.get_channel(int(category_id)))
        
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
        view = TicketSolvingButtons(ticket_id, category, FuncBot, log_channel_id)
        await ticket_channel.send(embed=info_embed, view=view)
        response_embed = discord.Embed(title="Ticket created!", description=f"Ticket created in {ticket_channel.mention}!", color=discord.Color.green())
        ticket_id += 1
        
        # Returns response embed
        return response_embed
    
    except Exception as e:
        console_log(f"There was an error while creating the ticket! Error: {e}", "error")
        error_embed = discord.Embed(title="Error", description="There was an error while creating the ticket! Please contact the administrator!", color=discord.Color.red())
        return error_embed
def has_opened_ticket(user_id: int) -> int | bool:
    """
    Checks if a user currently has an open ticket.

    Returns:
        True if user has an open ticket,
        False if not,
        -1 if error.
    """
    try:
        with get_session() as session:
            open_ticket = (
                session.query(DiscordTicket)
                .filter(DiscordTicket.Discord_ID == user_id, DiscordTicket.Opened == True)
                .first()
            )
            return bool(open_ticket)
    except Exception as e:
        console_log(f"Error checking open tickets: {e}", "error")
        return -1
def save_ticket_to_db(user_id: int) -> int:
    """
    Creates a new ticket record and returns its Ticket_ID.
    Returns -1 on error.
    """
    try:
        with get_session() as session:
            new_ticket = DiscordTicket(Discord_ID=user_id)
            session.add(new_ticket)
            session.commit()
            session.refresh(new_ticket)
            return new_ticket.Ticket_ID
    except Exception as e:
        console_log(f"Error while saving ticket: {e}", "error")
        return -1
async def claim_ticket(ticket_id: int, staff: discord.User, channel: discord.TextChannel) -> bool | discord.Embed:
    """
    Marks a ticket as claimed and updates Discord permissions.
    Returns True if successful or an error embed if failed.
    """
    try:
        with get_session() as session:
            ticket = session.query(DiscordTicket).filter_by(Ticket_ID=ticket_id).first()
            if not ticket:
                raise ValueError(f"Ticket {ticket_id} not found in DB.")

            ticket.Claimed_by = str(staff.id)
            session.commit()

        await channel.set_permissions(staff, read_messages=True, send_messages=True)
        topic = (channel.topic or "") + f" | Claimed by: {staff.mention}"
        await channel.edit(topic=topic)

        return True

    except Exception as e:
        console_log(f"Error while claiming the ticket: {e}", "error")
        return discord.Embed(
            title="Error",
            description="There was an error while claiming the ticket! Please try again or contact the administrator!",
            color=discord.Color.red()
        )
def check_if_allowed_to_claim(category: dict, user_roles: list[discord.Role]) -> bool | int:
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
def check_if_allowed_to_delete(interaction_user: discord.User, claimed_user: discord.User, category: dict) -> bool | int:
    # False = user is not allowed
    # True = user is allowed
    # -1 = error
    try:
        if interaction_user == claimed_user and claimed_user != False:
            return True
        else:
            roles = interaction_user.roles
            for role in roles:
                if role.permissions.administrator or str(role.id) in category['allowed_roles']:
                    return True
            return False
    except Exception as e:
        console_log(f"There was an error while checking if user is allowed to delete the ticket! Error: {e}", "error")
        return -1
async def log_ticket(channel: discord.TextChannel, category: dict, ticket_id: int, FuncBot: discord.Client) -> tuple[str | int, str | int]:
    """
    Logs all messages in a ticket channel (except bot messages) to the database.
    Returns (log_text, form_log_text) or (-1, -1) on error.
    """
    try:
        messages = [m async for m in channel.history(limit=None)]
        messages.reverse()

        log = ""
        form_log = ""

        for message in messages:
            if message.author != FuncBot.user:
                log += f"{message.author}: {message.content}\n"
            elif message.embeds:
                for field in message.embeds[0].fields:
                    if field.name != category["name"]:
                        value = field.value.strip("`")
                        form_log += f"{field.name}: {value}\n"

        # Save to DB
        with get_session() as session:
            log_entry = DiscordTicketLog(
                Ticket_ID=ticket_id,
                Category=category["name"],
                Transcript=log
            )
            session.add(log_entry)

        return log, form_log

    except Exception as e:
        console_log(f"There was an error while logging the ticket: {e}", "error")
        return -1, -1
async def delete_ticket(interaction: discord.Interaction, ticket_id: int, staff: discord.User, channel: discord.TextChannel, category: dict, FuncBot: discord.Client, log_channel_id: int) -> None:
    """
    Marks the ticket as closed, logs its contents, sends transcripts,
    and deletes the Discord channel.
    """
    embed = discord.Embed(
        title="Status",
        description=f"Deleting ticket-{ticket_id}...",
        color=discord.Color.red()
    )
    status_msg = await interaction.channel.send(embed=embed)

    try:
        with get_session() as session:
            ticket = session.query(DiscordTicket).filter_by(Ticket_ID=ticket_id).first()
            if not ticket:
                raise ValueError(f"Ticket {ticket_id} not found in database.")

            ticket.Opened = False
            user = FuncBot.get_user(int(ticket.Discord_ID))
            session.commit()

        embed.description = f"Ticket-{ticket_id} marked as closed!"
        embed.color = discord.Color.green()
        await status_msg.edit(embed=embed)

        log, form_log = await log_ticket(channel, category, ticket_id, FuncBot)
        if log == -1:
            raise Exception("Error while logging ticket.")

        log_embed = discord.Embed(
            title=f"Ticket-{ticket_id}",
            description=f"Ticket created by {user.mention}",
            color=discord.Color.green()
        )
        log_embed.add_field(name=category["name"], value=category["description"], inline=True)

        transcript_content = ""
        if form_log:
            transcript_content += f"Form:\n\n{form_log}\n----------------------------\n"
        transcript_content += f"Transcript:\n\n{log or 'No messages in this ticket.'}"

        file = io.StringIO(transcript_content)
        log_embed.set_thumbnail(url=user.avatar.url if user.avatar else discord.Embed.Empty)

        closer = staff.name if staff else interaction.user.name
        log_embed.set_footer(text=f"Ticket closed by {closer}")

        log_channel = FuncBot.get_channel(int(log_channel_id))
        await log_channel.send(embed=log_embed)
        await log_channel.send(file=discord.File(file, filename=f"Ticket-{ticket_id}.txt"))

        try:
            await user.send(embed=log_embed)
            await user.send(file=discord.File(file, filename=f"Ticket-{ticket_id}.txt"))
        except Exception as e:
            console_log(f"Could not send ticket log to user {user}. Error: {e}", "warning")

        try:
            if staff:
                await staff.send(embed=log_embed)
                await staff.send(file=discord.File(file, filename=f"Ticket-{ticket_id}.txt"))
        except Exception as e:
            console_log(f"Could not send ticket log to staff {staff}. Error: {e}", "warning")

        await channel.delete()

    except Exception as e:
        console_log(f"There was an error while deleting the ticket: {e}", "error")
        error_embed = discord.Embed(
            title="Error",
            description="There was an error while deleting the ticket! Please try again or contact the administrator!",
            color=discord.Color.red()
        )
        await status_msg.edit(embed=error_embed)
async def get_first_five_messages(channel: discord.TextChannel) -> list[discord.Message]:
    # Fetch a larger set of messages
    messages = []
    async for message in channel.history(limit=None):
        messages.append(message)

    # Sort messages by their creation time in ascending order
    messages.reverse()

    # Get the first five messages
    first_five_messages = messages[:5]
    return first_five_messages
async def tickets_on_restart(category_id: int, FuncBot: discord.Client, categories: dict, log_channel_id: int) -> None:
    # Checks if there are any opened tickets in category and if there are, it updates embeds, so they have working buttons
    try:
        category = FuncBot.get_channel(int(category_id))
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
                        # topic[1] is "Claimed by: {user mention}"
                        if len(topic) == 2:
                            # Gets user from topic
                            claimed = topic[1][14:-1]
                            claimed = FuncBot.get_user(int(claimed))
                        view = TicketSolvingButtons(int(channel.name[7:]), categories[category], FuncBot, log_channel_id, claimed)
                        await message.edit(view=view)
        except Exception as e:
            console_log(f"Something went wrong while getting the message! Error: {e}", "error")
            continue