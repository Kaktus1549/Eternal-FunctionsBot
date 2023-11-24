# Documentation for Eternal Gaming Function Bot

This is documentation for Eternal Gaming Function Bot. This bot is used for managing VIPs, showing leaderboard and staff information. Bot is written in Python and uses library discord.py and others located in requirements.txt. Bot imports config.json from folder ./config. If file is not found, bot will create one with default values.

## Config

If config.json is not found, bot will create one with default values:
```json
{
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
```

Config is divided into 4 sections: discord_settings, vip_settings, leader_settings and info_settings. discord_settings contains values of token, prefix for bot and role that can sync slash commands. vip_settings contains values for role that is allowed to remove VIPs, location of file with VIPs and ID of roles with VIP. leader_settings contains values for leaderboard channel, message and location of file with stats. info_settings contains values for bot info channel, message and location of file with hiearchy. Message limit is how many messages will be check and eventually deleted in channel.

## VIP

VIP section has multiple functions. Here is list and description of them:

### load_vips()

- Loads VIPs from file specified in config.json
- Can return 3 values: <br>
    - Array called data (contains data from VIPs file) <br>
    - 1 which means error <br>
    - 2 which means file not found/empty

### steamid_validation(steamid)

- As input takes steamID
- Does validation of steamID based on regex 
```python
pattern = r'^\d+@steam$'
match = re.match(pattern, steamid)
```
- If steamID is valid, return 0
- If steamID is not valid, return 1

### user_check(steamid, discord_id)

- As input takes steamID and discordID
- Loads VIPs and then checks if discordID or steamID is already present in VIPs
- Some VIPs (Donator and Sponzor) can have multiple steamIDs on one discordID, others can't
- Returns multiple values: <br>
    - False if either discordID and steamID is not present in VIPs <br>
    - 1 if discordID has VIP activeted <br>
    - 2 if steamID has VIP activeted <br>
    - 3 means error <br>

### user_add(steamid, discord_id, vip_role)

- As input takes steamID, discordID and role
- Expects that user_check() was already called and returned False
- Adds new VIP to VIPs
- Changes steamID to !steamID so David's plugin can assign values to benefits
- Then adds new VIP to VIPs and saves it
- Example of VIPs file:
```json
{
    "UserId":"!<steamID>", 
    "DiscordID":<DiscordID>, 
    "RoleType":<type>, 
    "VipAdvantageData":{
        "AvailableAdvantages":{}
    }, 
    "ExpirationDate":<unix timestamp in seconds>}
```
- Returns 0 if everything went fine, 1 if there was error

### user_remove(id)

- As input takes discordID or steamID
- Expects that discord user who used command has right to remove VIPs
- Loads VIPs and then checks if discordID or steamID is already present in VIPs
- If yes, removes it and saves VIPs
- Returns 0 if everything went fine, 1 if there was error and 2 if user was not found


## Leaderboard

Leaderboard section has multiple functions. Here is list and description of them:

### user_stats(user)

- As input takes SteamID or steam name
- Loads stats from file specified in config.json
- Checks if user is present in stats
- Returns:
    - -1 if stats file was not found
    - -2 if user was not found
    - UserID, Username, SCPKills, HumanKills, Deaths, TotalSeconds if user was found
    ```python
        UserID = user_statistics['UserID']
        Username = user_statistics['Username']
        SCPKills = user_statistics['SCPKills']
        HumanKills = user_statistics['HumanKills']
        Deaths = user_statistics['Deaths']
        TotalSeconds = user_statistics['TotalSeconds']
        return UserID, Username, SCPKills, HumanKills, Deaths, TotalSeconds
    ```

### get_stats(type)

- As input takes type of stats (SCP, Human, Deaths, Playtime)
- Loads stats from file specified in config.json
- Returns:
    - -1 if stats file was not found
    - -2 if type was not found
    - TOP 10 players in that category
    ```python
        top_10 = sorted_statistics[:10]
        return top_10
    ```

### all_players_list(index)

- As input takes index of page
- Loads stats from file specified in config.json and sorts them by total score
- Then it splits them into pages (10 players per page)
- Returns:
    - -1 if stats file was not found
    - -2 if stats file is empty
    - array called return_list with 10 players on page

### get_pages()

- As input takes nothing
- Loads stats from file specified in config.json 
- Calculates how many pages are there
- Returns:
    - -1 if stats file was not found
    - -2 if stats file is empty
    - number of pages

### discord.ui

There are also classes for buttons, basically there is main board in channel with buttons, in this class is specified button text and what it does. Example:
```python  
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
```
