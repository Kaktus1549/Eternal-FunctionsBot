from GlobalUtils.utils import console_log, is_steamid
import discord
from VIPs.vip_utils import user_check, user_add, user_update, user_remove


async def vipactivate(ctx: discord.Interaction, steam_id: str="-1", roles: dict | None = None) -> None:
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
    for i in roles:
        if found_role == True:
            break
        if roles[i]["RoleID"] == "ROLE_ID":
            console_log(f"Role {i} has not been set in settings.json!", "error")
            return_message = "Disocrd bot has not been configured correctly, please contact bot owner!"
        else:
            for user_role in user_roles:
                if roles[i]["RoleID"] == str(user_role.id):
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

        exists, msg = user_check(steamid, ctx.author.id, vip_status, roles)
        if msg is not None:
            if msg.startswith("Error"):
                exception_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
                exception_embed.set_thumbnail(url=ctx.author.avatar.url)
                exception_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
                await return_embed.edit(content=None, embed=exception_embed)
                return
            else:
                # User never joined the server before
                no_join_embed = discord.Embed(title="VIP activation failed!", description=msg, color=0xff0000)
                no_join_embed.add_field(name="Action required", value="Join the SCP:SL server at least once before activating VIP!", inline=True)
                no_join_embed.set_thumbnail(url=ctx.author.avatar.url)
                await return_embed.edit(content=None, embed=no_join_embed)
        if exists == 0:
            try:
                status, msg = user_add(steamid, ctx.author.id, vip_status)
                console_log(f"Adding VIP for user {ctx.author.name}, status: {status}, msg: {msg}", "info")
                if status == True:
                    console_log(f"VIP for user {ctx.author.name} has been activated!", "info")
                    vip_embed = discord.Embed(title="VIP activated!", description=f"VIP has been activated for user {ctx.author.name}!", color=0x00ff00)
                    vip_embed.set_thumbnail(url=ctx.author.avatar.url)
                    vip_embed.add_field(name="SteamID", value=steamid, inline=True)
                    vip_embed.add_field(name="VIP role", value=vip_status, inline=True)
                    return_embed = await return_embed.edit(content=None ,embed=vip_embed)
                else:
                    console_log(f"Error while activating VIP for user {ctx.author.name}: {msg}", "error")
                    error_vip_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
                    error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
                    error_vip_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
                    await return_embed.edit(content=None, embed=error_vip_embed)
            except Exception as error:
                console_log(f"Exception while activating VIP for user {ctx.author.name}: {error}", "error")
                exception_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
                exception_embed.set_thumbnail(url=ctx.author.avatar.url)
                exception_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
                await return_embed.edit(content=None, embed=exception_embed)
        elif exists == 1:
            update_embed = discord.Embed(title="VIP in progress!", description=return_message, color=discord.Color.dark_grey())
            update_embed.add_field(name="Status", value="Found higher VIP role, updating...", inline=True)
            return_embed = await return_embed.edit(content=None, embed=update_embed)
            try:
                status, msg = user_update(steamid, vip_status)
                if status == True:
                    console_log(f"VIP for user {ctx.author.name} has been updated!", "info")
                    vip_embed = discord.Embed(title="VIP updated!", description=f"VIP has been updated for user {ctx.author.name}!", color=0x00ff00)
                    vip_embed.set_thumbnail(url=ctx.author.avatar.url)
                    vip_embed.add_field(name="SteamID", value=steamid, inline=True)
                    vip_embed.add_field(name="VIP role", value=vip_status, inline=True)
                    return_embed = await return_embed.edit(content=None ,embed=vip_embed)
                else:
                    if msg.startswith("Player with SteamID "):
                        console_log(f"Error while updating VIP for user {ctx.author.name}: {msg}", "error")
                        no_join_embed = discord.Embed(title="VIP activation failed!", description=msg, color=0xff0000)
                        no_join_embed.add_field(name="Action required", value="Join the SCP:SL server at least once before activating VIP!", inline=True)
                        no_join_embed.set_thumbnail(url=ctx.author.avatar.url)
                        await return_embed.edit(content=None, embed=no_join_embed)
                    else:
                        error_vip_embed = discord.Embed(title="Error!", description=f"An error has occured while activating VIP for user {ctx.author.name}!", color=0xff0000)
                        error_vip_embed.set_thumbnail(url=ctx.author.avatar.url)
                        error_vip_embed.add_field(name="Something went wrong!", value="Try again later or contact bot owner!", inline=True)
                        await return_embed.edit(content=None, embed=error_vip_embed)
            except Exception as error:
                console_log(f"Exception while updating VIP for user {ctx.author.name}: {error}", "error")
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
async def removevip(ctx: discord.Interaction, id: str="-1", removers: str = "") -> None:
    if id == "-1":
        invalid_id_embed = discord.Embed(title="Invalid ID!", description="Please provide valid SteamID or DiscordID!", color=0xff0000)
        await ctx.send(embed=invalid_id_embed)
        return
    allowed_users = removers.split(', ')
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
        remove, msg = user_remove(remove_user_id)
        if remove == True:
            console_log(f"VIP has been removed for id {remove_user_id} by {ctx.author.name}", "info")
            success_embed = discord.Embed(title="Success!", description=f"VIP has been removed for id **{remove_user_id}**!", color=0x00ff00)
            await ctx.send(embed=success_embed)
        elif msg is not None and msg.startswith("Player '"):
            error_embed = discord.Embed(title="Error!", description=f"Provided ID **{remove_user_id}** has no VIP!", color=0xff0000)
            await ctx.send(embed=error_embed)
        else:
            console_log(f"Error while removing VIP for id {remove_user_id}: {msg}", "error")
            error_embed = discord.Embed(title="Error!", description=f"An error has occured while removing VIP for id **{remove_user_id}**!", color=0xff0000)
            await ctx.send(embed=error_embed)
    else:
        console_log(f"{ctx.author.name} has tried to remove VIP from user {id}, but doesn't have permission!", "info")
        error_embed = discord.Embed(title="Error!", description="You don't have permission to use this command!", color=0xff0000)
        await ctx.send(embed=error_embed)