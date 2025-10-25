import discord
#from Statistics.statistics_utils import get_stats, all_players_list, get_pages
from StaffList.staff_list_utils import print_subdepartments, color_from_hierarchy
from EternalBot.help_utils import info_help, leader_help, vip_help, ticket_help
from GlobalUtils.utils import console_log

# class LeaderButtons(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
    
#     @discord.ui.button(label="SCP Kills", style=discord.ButtonStyle.red, custom_id="scp")
#     async def scp_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
#         SCPKills = get_stats("ScpKills")
#         if SCPKills == -1:
#             error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         elif SCPKills == -2:
#             error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         else:
#             stats_embed = discord.Embed(title="Top 10 SCP Kills", description="Tady je top 10 hráčů s nejvíce zabitymi SCP", color=0xff0000)
#             for i in range(len(SCPKills)):
#                 stats_embed.add_field(name=f"{i+1}. __{SCPKills[i][0]}__", value=f"**SCP Kills:** {SCPKills[i][1]}", inline=False)
#             await interaction.response.send_message(embed=stats_embed, ephemeral=True)
#             return
#     @discord.ui.button(label="Human Kills", style=discord.ButtonStyle.blurple, custom_id="human")
#     async def human_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
#         HumanKills = get_stats("PlayerKills")
#         if HumanKills == -1:
#             error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         elif HumanKills == -2:
#             error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         else:
#             stats_embed = discord.Embed(title="Top 10 Human Kills", description="Tady je top 10 hráčů s nejvíce zabitymi hráči za lidskou roli", color=discord.Color.blurple())
#             for i in range(len(HumanKills)):
#                 stats_embed.add_field(name=f"{i+1}. __{HumanKills[i][0]}__", value=f"**Human Kills:** {HumanKills[i][1]}", inline=False)
#             await interaction.response.send_message(embed=stats_embed, ephemeral=True)
#             return
#     @discord.ui.button(label="Deaths", style=discord.ButtonStyle.gray, custom_id="deaths")
#     async def deaths_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
#         Deaths = get_stats("Deaths")
#         if Deaths == -1:
#             error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         elif Deaths == -2:
#             error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         else:
#             stats_embed = discord.Embed(title="Top 10 Deaths", description="Tady je top 10 hráčů s nejvíce deaths", color=discord.Color.dark_gray())
#             for i in range(len(Deaths)):
#                 stats_embed.add_field(name=f"{i+1}. __{Deaths[i][0]}__", value=f"**Deaths:** {Deaths[i][1]}", inline=False)
#             await interaction.response.send_message(embed=stats_embed, ephemeral=True)
#             return
#     @discord.ui.button(label="Time", style=discord.ButtonStyle.green, custom_id="time")
#     async def time_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
#         Time = get_stats("PlayedSeconds")
#         if Time == -1:
#             error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         elif Time == -2:
#             error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         else:
#             stats_embed = discord.Embed(title="Top 10 Time", description="Tady je top 10 hráčů s nejdelší dobou na serveru", color=discord.Color.green())
#             for i in range(len(Time)):
#                 time_in_seconds = Time[i][1]
#                 TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
#                 stats_embed.add_field(name=f"{i+1}. __{Time[i][0]}__", value=f"**Time:** {TotalTime}", inline=False)
#             await interaction.response.send_message(embed=stats_embed, ephemeral=True)
#             return
# class InteractiveLeaderboard(discord.ui.View):
#     def __init__(self, messageEmbed, pageNumber=1):
#         super().__init__(timeout=600)
#         self.listValue = (pageNumber - 1) * 10
#         self.embed = messageEmbed
    
#     @discord.ui.button(label="⬅️ Previous", style=discord.ButtonStyle.red)
#     async def previous_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
#         self.listValue = self.listValue - 10
#         if self.listValue < 0:
#             self.listValue = 0
#             players_list = all_players_list(self.listValue)
#         else:
#             players_list = all_players_list(self.listValue)
#         if players_list == -1:
#             error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         elif players_list == -2:
#             error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         else:
#             new_embed = discord.Embed(title="All players in one leaderboard", description="Tady jsou všichni hráči na jednom leaderboardu", color=discord.Color.dark_blue())
#             new_embed.set_thumbnail(url=interaction.guild.icon)
#             for i in range(len(players_list)):
#                 time_in_seconds = players_list[i][4]
#                 TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
#                 new_embed.add_field(name=f"{i+1+self.listValue}. __{players_list[i][0]}__", value=f"Odehraný čas: {TotalTime} <==> Počet smrtí: {players_list[i][3]}\nPočet zabitých SCP: {players_list[i][1]} <======> Počet zabitých hráčů: {players_list[i][2]}", inline=False)
#             new_embed.set_footer(text=f"Page {self.listValue // 10 + 1}/{get_pages()}")
#             await interaction.response.edit_message(embed=new_embed, view=self)
#     @discord.ui.button(label="Next ➡️", style=discord.ButtonStyle.red)
#     async def next_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
#         self.listValue = self.listValue + 10
#         if (self.listValue // 10) > (get_pages() - 1):
#             self.listValue = self.listValue - 10
#             players_list = all_players_list(self.listValue)
#         else:
#             players_list = all_players_list(self.listValue)
#         if players_list == -1:
#             error_embed = discord.Embed(title="Error", description="There is something wrong with the config file, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         elif players_list == -2:
#             error_embed = discord.Embed(title="Error", description="Something went wrong while getting the stats, please contact the administrator", color=0xff0000)
#             await interaction.response.send_message(embed=error_embed, ephemeral=True)
#             return
#         else:
#             new_embed = discord.Embed(title="All players in one leaderboard", description="Tady jsou všichni hráči na jednom leaderboardu", color=discord.Color.dark_blue())
#             new_embed.set_thumbnail(url=interaction.guild.icon)
#             for i in range(len(players_list)):
#                 time_in_seconds = players_list[i][4]
#                 TotalTime = f"{time_in_seconds // 3600}h {time_in_seconds % 3600 // 60}m {time_in_seconds % 3600 % 60}s"
#                 new_embed.add_field(name=f"{i+1+self.listValue}. __{players_list[i][0]}__", value=f"Odehraný čas: {TotalTime} <==> Počet smrtí: {players_list[i][3]}\nPočet zabitých SCP: {players_list[i][1]} <======> Počet zabitých hráčů: {players_list[i][2]}", inline=False)
#             new_embed.set_footer(text=f"Page {self.listValue // 10 + 1}/{get_pages()}")
#             await interaction.response.edit_message(embed=new_embed, view=self)
class InfoButtons(discord.ui.View):
    def __init__(self, buttons_config, hierarchy_file="config/hierarchy.json", hierarchy_encoding="utf-8"):
        super().__init__(timeout=None)
        if buttons_config == -1:
            return -1
        self.buttons_config = buttons_config
        self.hierarchy_file = hierarchy_file
        self.hierarchy_encoding = hierarchy_encoding

        for button_data in buttons_config: 
            label = buttons_config[button_data]['button_text']
            color = color_from_hierarchy(buttons_config[button_data]['button_color'], True)
            custom_id = button_data
            button = discord.ui.Button(label=label, custom_id=custom_id, style=color)
            button.callback = self.button_callback
            self.add_item(button)
    
    async def button_callback(self, interaction: discord.Interaction):
        button_embed = print_subdepartments(interaction.data['custom_id'], interaction.guild, self.hierarchy_file, self.hierarchy_encoding)
        await interaction.response.send_message(embed=button_embed, ephemeral=True)
class HelpButtons(discord.ui.View):
    def __init__(self, messageEmbed, help_type, ctx=None, *args, **kwargs):
        super().__init__(timeout=180)
        self.embed = messageEmbed
        self.help_type = help_type
        self.ctx = ctx
        self.bot_avatar = kwargs.get("bot_avatar")
        self.allowed_roles = kwargs.get("allowed_roles")
        self.info_channel_id = kwargs.get("info_channel_id")
        self.staff_enabled = kwargs.get("staff_enabled")
        self.statistics_enabled = kwargs.get("statistics_enabled")
        self.statistics_channel_id = kwargs.get("statistics_channel_id")
        self.vip_enabled = kwargs.get("vip_enabled")
        self.ticket_enabled = kwargs.get("ticket_enabled")

        self.kwargs = kwargs

    @discord.ui.button(label="❔ Info help", style=discord.ButtonStyle.red)
    async def info_help_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.help_type == "info":
            return
        else:
            await interaction.response.edit_message(embed=info_help(self.ctx, self.bot_avatar, self.allowed_roles, self.info_channel_id, self.staff_enabled), view=HelpButtons(info_help(self.ctx, self.bot_avatar, self.allowed_roles, self.info_channel_id, self.staff_enabled), "info", self.ctx, **self.kwargs))
    @discord.ui.button(label="📊 LeaderBoard help", style=discord.ButtonStyle.blurple)
    async def leader_help_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.help_type == "leader":
            return
        else:
            await interaction.response.edit_message(embed=leader_help(self.ctx, self.bot_avatar, self.statistics_enabled, self.statistics_channel_id), view=HelpButtons(leader_help(self.ctx, self.bot_avatar, self.statistics_enabled, self.statistics_channel_id), "leader", self.ctx, **self.kwargs))
    @discord.ui.button(label="💶 VIP help", style=discord.ButtonStyle.green)
    async def vip_help_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.help_type == "vip":
            return
        else:
            await interaction.response.edit_message(embed=vip_help(self.ctx, self.bot_avatar, self.vip_enabled), view=HelpButtons(vip_help(self.ctx, self.bot_avatar, self.vip_enabled), "vip", self.ctx, **self.kwargs))
    @discord.ui.button(label="📩 Ticket help", style=discord.ButtonStyle.gray)
    async def ticket_help_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.help_type == "ticket":
            return
        else:
            await interaction.response.edit_message(embed=ticket_help(self.ctx, self.bot_avatar, self.ticket_enabled), view=HelpButtons(ticket_help(self.ctx, self.bot_avatar, self.ticket_enabled), "ticket", self.ctx, **self.kwargs))
class TicketModal(discord.ui.Modal):
    def __init__(self, category: dict, guild: discord.Guild, user: discord.User, category_id: int, categories: dict, log_channel_id: int, FuncBot: discord.Client):
        self.guild = guild
        self.user = user
        self.category = category
        self.category_id = category_id
        self.categories = categories
        self.log_channel_id = log_channel_id
        self.FuncBot = FuncBot
        super().__init__(timeout=None, title="Ticket form")

        i = 0
        for question in category['modal_questions']:
            if i >= 5:
                break

            question_data = category['modal_questions'][question]
            mandatory = question_data['mandatory']
            label = question_data['label']
            placeholder = question_data['placeholder']
            style = discord.TextStyle.long if question_data['style'] == "text" else discord.TextStyle.short

            input_field = discord.ui.TextInput(
                label=label,
                placeholder=placeholder,
                style=style,
                required=mandatory,
                custom_id=label
            )
            self.add_item(input_field)
            i += 1
    async def on_submit(self, interaction: discord.Interaction):
        from Tickets.tickets_utils import create_ticket
        try:
            form_result = {}

            for item in self.children:
                if isinstance(item, discord.ui.TextInput):
                    form_result[item.custom_id] = item.value

            embed = await create_ticket(self.guild, self.category, self.user, self.category_id, self.categories, self.FuncBot, self.log_channel_id, form_result)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            console_log(f"Something went wrong while creating the ticket! Error: {e}", "error")
            error_embed = discord.Embed(title="Error", description="Something went wrong while creating the ticket, please contact the administrator!", color=discord.Color.red())
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
class TicketDropdown(discord.ui.Select):
    def __init__(self, categories: dict, placeholder: str, category_id: int, FuncBot: discord.Client, log_channel_id: int, informative: bool = True):
        options = []
        self.informative = informative
        self.categories = categories
        self.category_id = category_id
        self.FuncBot = FuncBot
        self.log_channel_id = log_channel_id
        for category in categories:
            options.append(discord.SelectOption(label=category))
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.informative:
            if self.values[0] not in self.categories:
                error_embed= discord.Embed(title="Error", description="Got mismatched category, please try again!", color=discord.Color.red())
                await interaction.response.edit_message(embed=error_embed)
            else:
                category = self.values[0]
                view = TicketDropdownView(self.categories, category)
                category_embed = discord.Embed(title=f"{category}", description=f"{self.categories[category]['description']}", color=discord.Color.blurple())
                role_mentions = ""
                for role in self.categories[category]['allowed_roles']:
                    role_mentions += f"<@&{role}> "
                category_embed.add_field(name="Staff who will handle your ticket:", value=role_mentions, inline=False)
                await interaction.response.edit_message(embed=category_embed, view=view)
        else:
            if self.values[0] not in self.categories:
                error_embed = discord.Embed(title="Error", description="Got mismatched category, please try again!", color=discord.Color.red())
                await interaction.response.edit_message(embed=error_embed)
            else:
                category = self.values[0]
                modal = TicketModal(self.categories[category], interaction.guild, interaction.user, self.category_id, self.categories, self.log_channel_id, self.FuncBot)
                await interaction.response.send_modal(modal)
class TicketDropdownView(discord.ui.View):
    def __init__(self, categories: dict, category_id: int, FuncBot: discord.Client, log_channel_id: int, placeholder: str = "Select category", informative: bool = True):
        super().__init__(timeout=None)
        if categories == 1 or categories == None:
            self.categories = {}
        self.categories = categories
        self.category_id = category_id
        dropdown = TicketDropdown(categories, placeholder, category_id, FuncBot, log_channel_id, informative)
        self.add_item(dropdown)
class TicketButtons(discord.ui.View):
    def __init__(self, categories: dict, category_id: int, FuncBot: discord.Client, log_channel_id: int):
        super().__init__(timeout=None)
        if categories == 1 or categories == None:
            self.categories = {}
        self.categories = categories
        self.category_id = category_id
        self.FuncBot = FuncBot
        self.log_channel_id = log_channel_id

    @discord.ui.button(label="📩 Open ticket", style=discord.ButtonStyle.red)
    async def open_ticket_on_click(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.categories == {}:
            no_categories = discord.Embed(title="Error", description="I can't find any categories, please contact the administrator!", color=discord.Color.red())
            await interaction.response.send_message(embed=no_categories, ephemeral=True)
            return
        else:
            view = TicketDropdownView(self.categories, category_id=self.category_id, FuncBot=self.FuncBot, log_channel_id=self.log_channel_id, informative=False)
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
            view = TicketDropdownView(self.categories, category_id=self.category_id, FuncBot=self.FuncBot, log_channel_id=self.log_channel_id)
            await interaction.response.send_message(embed=categories_embed, view=view, ephemeral=True)
class TicketSolvingButtons(discord.ui.View):
    def __init__(self, ticket_id: int, category: str, FuncBot: discord.Client, log_channel_id: int, claimed=False):
        super().__init__(timeout=None)
        self.ticket_id = ticket_id
        self.category = category
        self.FuncBot = FuncBot
        self.log_channel_id = log_channel_id
        self.claimed = claimed
        # Add the "Claim Ticket" button only if the ticket has not been claimed
        if self.claimed == False:
            claim_ticket_button = discord.ui.Button(label="🔧 Claim ticket", style=discord.ButtonStyle.green)
            claim_ticket_button.callback = self.claim_ticket_on_click
            self.add_item(claim_ticket_button)
        # Add the "Close Ticket" button
        close_ticket_button = discord.ui.Button(label="🔒 Close ticket", style=discord.ButtonStyle.red)
        close_ticket_button.callback = self.close_ticket_on_click
        self.add_item(close_ticket_button)

    async def claim_ticket_on_click(self, interaction: discord.Interaction):
        try:
            from Tickets.tickets_utils import check_if_allowed_to_claim, claim_ticket
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
                return
            if not allowed:
                await interaction.response.send_message(embed=discord.Embed(title="Error", description="You are not allowed to claim this ticket!", color=discord.Color.red()), ephemeral=True)
            else:
                await interaction.response.send_message(embed=discord.Embed(title="Error", description="Something went wrong while claiming the ticket, please contact the administrator!", color=discord.Color.red()), ephemeral=True)
        except Exception as e:
            console_log(f"Something went wrong while claiming the ticket! Error: {e}", "error")
            await interaction.response.send_message(embed=discord.Embed(title="Error", description="Something went wrong while claiming the ticket, please contact the administrator!", color=discord.Color.red()), ephemeral=True)
    async def close_ticket_on_click(self, interaction: discord.Interaction):
        try:
            from Tickets.tickets_utils import check_if_allowed_to_delete, delete_ticket
            allowed = check_if_allowed_to_delete(interaction.user, self.claimed, self.category)
            
            if allowed == True:
                await delete_ticket(interaction, self.ticket_id, self.claimed, interaction.channel, self.category, self.FuncBot, self.log_channel_id)
                return
            if allowed == False:
                await interaction.response.send_message(embed=discord.Embed(title="Error", description="You are not allowed to close this ticket!", color=discord.Color.red()), ephemeral=True)
                return
            if allowed != True and allowed != False and allowed != -1:
                await interaction.response.send_message(embed=discord.Embed(title="Error", description="Something went wrong while closing the ticket, please contact the administrator!", color=discord.Color.red()), ephemeral=True)
                return
        except Exception as e:
            console_log(f"Something went wrong while closing the ticket! Error: {e}", "error")
            await interaction.response.send_message(embed=discord.Embed(title="Error", description="Something went wrong while closing the ticket, please contact the administrator!", color=discord.Color.red()), ephemeral=True)