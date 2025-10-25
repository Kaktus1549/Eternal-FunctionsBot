from StaffList.staff_list_utils import open_hiearchy, save_hiearchy, check_roles
import discord

async def priority(ctx: discord.Interaction, department: str = "-1", priority: str = "-1", hiearchy_file: str = "./config/hiearchy.json", hiearchy_encoding: str = "utf-8", allowed_roles: list = ["978277386091102218"]) -> None:
    if not check_roles(ctx.author, allowed_roles):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if department == "-1" or priority == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the department and the priority!", color=discord.Color.red()))
        return
    if priority is not int and priority.isnumeric() == False:
        await ctx.send(embed=discord.Embed(title="Error", description="Priority needs to be a number!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy(hiearchy_file, hiearchy_encoding)
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        hiearchy[department]['settings'][2] = int(priority)
        save_hiearchy(hiearchy, hiearchy_file, hiearchy_encoding)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Priority of {department} was set to {priority}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while setting the priority: {e}", color=discord.Color.red()))
        return
async def add_department(ctx: discord.Interaction, name: str = "-1", color: str = "grey", text: str = "-1", priority: str = "1000", hiearchy_file: str = "./config/hiearchy.json", hiearchy_encoding: str = "utf-8", allowed_roles: list = ["978277386091102218"]) -> None:
    priority = str(priority)
    if not check_roles(ctx.author, allowed_roles):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if name == "-1" or text == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the color and the text!", color=discord.Color.red()))
        return
    if priority is not int and priority.isnumeric() == False:
        await ctx.send(embed=discord.Embed(title="Error", description="Priority needs to be a number!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy(hiearchy_file, hiearchy_encoding)
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        hiearchy[name] = {
            "settings": [color, text, priority]
        }
        save_hiearchy(hiearchy, hiearchy_file, hiearchy_encoding)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Department {name} was added!", color=discord.Color.green()))
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while adding the department: {e}", color=discord.Color.red()))
        return
async def remove_department(ctx: discord.Interaction, name: str = "-1", hiearchy_file: str = "./config/hiearchy.json", hiearchy_encoding: str = "utf-8", allowed_roles: list = ["978277386091102218"]) -> None:
    if not check_roles(ctx.author, allowed_roles):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the name!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy(hiearchy_file, hiearchy_encoding)
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        del hiearchy[name]
        save_hiearchy(hiearchy, hiearchy_file, hiearchy_encoding)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Department {name} was removed!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while removing the department: {e}", color=discord.Color.red()))
        return
async def update_department(ctx: discord.Interaction, name: str = "-1", color: str = "-1", text: str = "-1", hiearchy_file: str = "./config/hiearchy.json", hiearchy_encoding: str = "utf-8", allowed_roles: list = ["978277386091102218"]) -> None:
    if not check_roles(ctx.author, allowed_roles):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to tell me the name of the department!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy(hiearchy_file, hiearchy_encoding)
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        if color != "-1":
            hiearchy[name]['settings'][0] = color
        if text != "-1":
            hiearchy[name]['settings'][1] = text
        save_hiearchy(hiearchy, hiearchy_file, hiearchy_encoding)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Department {name} was updated!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while updating the department: {e}", color=discord.Color.red()))
        return
async def add_section(ctx: discord.Interaction, department: str = "-1", name: str = "-1", role: str = "-1", hiearchy_file: str = "./config/hiearchy.json", hiearchy_encoding: str = "utf-8", allowed_roles: list = ["978277386091102218"]) -> None:
    if not check_roles(ctx.author, allowed_roles):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if department == "-1" or name == "-1" or role == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the department, name and role!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy(hiearchy_file, hiearchy_encoding)
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        hiearchy[department][name] = role
        save_hiearchy(hiearchy, hiearchy_file, hiearchy_encoding)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Section {name} was added to {department}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while adding the section: {e}", color=discord.Color.red()))
        return
async def remove_section(ctx: discord.Interaction, department: str = "-1", name: str = "-1", hiearchy_file: str = "./config/hiearchy.json", hiearchy_encoding: str = "utf-8", allowed_roles: list = ["978277386091102218"]) -> None:
    if not check_roles(ctx.author, allowed_roles):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if department == "-1" or name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the department and the name!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy(hiearchy_file, hiearchy_encoding)
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        del hiearchy[department][name]
        save_hiearchy(hiearchy, hiearchy_file, hiearchy_encoding)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Section {name} was removed from {department}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department or section not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while removing the section: {e}", color=discord.Color.red()))
        return
async def update_section(ctx: discord.Interaction, department: str = "-1", name: str = "-1", role: str = "-1", hiearchy_file: str = "./config/hiearchy.json", hiearchy_encoding: str = "utf-8", allowed_roles: list = ["978277386091102218"]) -> None:
    if not check_roles(ctx.author, allowed_roles):
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    if department == "-1" or name == "-1" or role == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the department, name and role!", color=discord.Color.red()))
        return
    hiearchy = open_hiearchy(hiearchy_file, hiearchy_encoding)
    if hiearchy == -1:
        await ctx.send(embed=discord.Embed(title="Error", description="There was an error while opening the hiearchy file!", color=discord.Color.red()))
        return
    try:
        hiearchy[department][name] = role
        save_hiearchy(hiearchy, hiearchy_file, hiearchy_encoding)
        await ctx.send(embed=discord.Embed(title="Success", description=f"Section {name} was updated in {department}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Department or section not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while updating the section: {e}", color=discord.Color.red()))
        return  