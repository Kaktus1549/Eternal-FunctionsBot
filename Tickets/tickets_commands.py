import discord
from Tickets.tickets_utils import save_categories

async def add_category(ctx, name="-1", description="-1", roles="-1"):
    if name == "-1" or description == "-1" or roles == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the name, description and roles!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    try:
        input_roles = roles.split(",")
        roles = []
        for i in range(len(input_roles)):
            if input_roles[i].startswith('<@') and input_roles[i].endswith('>'):
                # Role mention is provided
                roles.append(input_roles[i][3:-1]) # Removing <@& and > from mention
            elif input_roles[i].isnumeric() == False:
                await ctx.send(embed=discord.Embed(title="Error", description="Roles need to be numbers or mentions!", color=discord.Color.red()))
                return
            else:
                roles.append(int(input_roles[i]))
        categories[name] = {
            "description": description,
            "allowed_roles": roles
        }
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Category {name} was added!", color=discord.Color.green()))
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while adding the category: {e}", color=discord.Color.red()))
        return
async def remove_category(ctx, name="-1"):
    if name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the name!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    try:
        del categories[name]
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Category {name} was removed!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Category not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while removing the category: {e}", color=discord.Color.red()))
        return
async def update_category(ctx, name="-1", description="-1", roles="-1"):
    if name == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to specify the name!", color=discord.Color.red()))
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    try:
        if roles != "-1":
            input_roles = input_roles.split(",")
            roles = []
            for i in range(len(input_roles)):
                if input_roles[i].isnumeric() == False:
                    await ctx.send(embed=discord.Embed(title="Error", description="Roles need to be numbers!", color=discord.Color.red()))
                    return
                else:
                    roles.append(int(input_roles[i]))
        else:
            roles = categories[name]['allowed_roles']
        if description == "-1":
            description = categories[name]['description']
        categories[name] = {
            "name": name,
            "description": description,
            "allowed_roles": roles
        }
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Category {name} was updated!", color=discord.Color.green()))
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while updating the category: {e}", color=discord.Color.red()))
        return
async def add_question(ctx, category="-1", question="-1", placeholder="-1", style="text", mandatory="false"):
    if category == "-1" or question == "-1" or placeholder == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the category, question, placeholder, style and mandatory!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    allowed_styles = ["text", "shorttext"]
    if style.lower() not in allowed_styles:
        await ctx.send(embed=discord.Embed(title="Error", description=f"Style needs to be one of these: {allowed_styles}", color=discord.Color.red()))
        return
    if mandatory.lower() == "true":
        mandatory = True
    elif mandatory.lower() == "false":
        mandatory = False
    else:
        await ctx.send(embed=discord.Embed(title="Error", description="Mandatory needs to be true or false!", color=discord.Color.red()))
        return
    try:
        categories[category]['modal_questions'][question] = {
            "label": question,
            "placeholder": placeholder,
            "style": style.lower(),
            "mandatory": mandatory
        }
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Question {question} was added to {category}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Category not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while adding the question: {e}", color=discord.Color.red()))
        return
async def remove_question(ctx, category="-1", question="-1"):
    if category == "-1" or question == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the category and the question!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    try:
        del categories[category]['modal_questions'][question]
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Question {question} was removed from {category}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Category or question not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while removing the question: {e}", color=discord.Color.red()))
        return
async def update_question(ctx, category="-1", question="-1", placeholder="-1", style="-1", mandatory="-1"):
    if category == "-1" or question == "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="You need to set the category and the question!", color=discord.Color.red()))
        return
    user_roles = ctx.author.roles
    for role in user_roles:
        if str(role.id) in settings['ticket_settings']['channel']['allowed_roles']:
            admin = True
            break
        else:
            admin = False
    if admin == False:
        await ctx.send(embed=discord.Embed(title="Error", description="You don't have permissions to use this command!", color=discord.Color.red()))
        return
    allowed_styles = ["text", "shorttext"]
    if style.lower() not in allowed_styles and style != "-1":
        await ctx.send(embed=discord.Embed(title="Error", description=f"Style needs to be one of these: {allowed_styles}", color=discord.Color.red()))
        return
    if mandatory.lower() == "true":
        mandatory = True
    elif mandatory.lower() == "false":
        mandatory = False
    elif mandatory != "-1":
        await ctx.send(embed=discord.Embed(title="Error", description="Mandatory needs to be true or false!", color=discord.Color.red()))
        return
    try:
        if placeholder != "-1":
            categories[category]['modal_questions'][question]['placeholder'] = placeholder
        if style != "-1":
            categories[category]['modal_questions'][question]['style'] = style.lower()
        if mandatory != "-1":
            categories[category]['modal_questions'][question]['mandatory'] = mandatory
        save_categories()
        await ctx.send(embed=discord.Embed(title="Success", description=f"Question {question} was updated in {category}!", color=discord.Color.green()))
    except KeyError:
        await ctx.send(embed=discord.Embed(title="Error", description="Category or question not found!", color=discord.Color.red()))
        return
    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Error", description=f"There was an error while updating the question: {e}", color=discord.Color.red()))
        return