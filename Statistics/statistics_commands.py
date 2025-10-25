import discord
from discord.ext import commands
from GlobalUtils.logging import console_log
from Statistics.statistics_utils import user_stats, all_players_list, get_pages
from EternalBot.DiscordUI.ui import InteractiveLeaderboard

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
