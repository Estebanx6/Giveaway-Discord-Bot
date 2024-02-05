import discord
from discord import message
from discord.ext import commands, tasks

import config
from config import *
import random

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix=config.prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print( "started")


participants = []
@bot.event
async def on_reaction_add(reaction, user):
    if user.id != bot.user.id:
        role = (discord.utils.get(user.roles, name=config.All_commands_role))
        if role:
            if message_warn and reaction.message.id == message_warn.id:   
                if reaction.emoji == "✅":
                    global can_create
                    can_create = True
                    await message_warn.delete()
                    embed.set_footer(text = "CANCELLED")
                    await message_give2.edit(embed = embed)
                    participants.clear()


                if reaction.emoji == "❎":
                    await message_warn.delete()


    else: 
        pass

    if reaction.message.id == message_give2.id and user.id not in participants:
        participants.append(user)



can_create = True
message_warn = None
@bot.command()
async def giveaway(ctx, award=None, winners=None):
    
    global can_create
    global message_warn
    global message_give2
    global embed
    global num_winners

    await ctx.message.delete()
    role = (discord.utils.get(ctx.author.roles, name=config.All_commands_role))
    if role:
        if can_create == True:
            try:
                winners = int(winners)
                num_winners = int(winners)
            except:
                message_error = await ctx.send("The command is '{}giveaway award winners'".format(config.prefix))
            else:
                if winners:
                    

                    embed = discord.Embed(title=f"**{award}**", color=0x5CDBF0, description=f"""
                Use the buttom: 🎉 to participate
                Hosted by: **{ctx.author.mention}**
                Winners: **{winners}**""")

                    message_give2 = await ctx.send(embed=embed)
                    await  message_give2.add_reaction("🎉")
                    can_create = False
                    participants.clear()
                else:
                    message_error = await ctx.send("The command is '{}giveaway award winners'".format(config.prefix))

        else:
            message_warn = await ctx.send("A giveaway already exists, do you want to delete it?")
            await message_warn.add_reaction("✅")
            await message_warn.add_reaction("❎")



def setcreate():
    global can_create
    can_create = True



@bot.command()
async def sort(ctx):
    await ctx.message.delete()
    role = (discord.utils.get(ctx.author.roles, name=config.All_commands_role))
    if role:
        if can_create == False:
            for i in range(num_winners):
                if participants == []:
                    break

                else:
                    win = random.choice(participants)
                    participants.remove(win)
                    await message_give2.channel.send("Congratulations " + win.mention + ", you **WON**!!!")

            embed.set_footer(text = "ENDED")
            await message_give2.edit(embed = embed)
            participants.clear()
            setcreate()





@bot.command()
async def help(ctx):
    await ctx.send(
f"""
`{config.prefix}giveaway - create new giveaway
{config.prefix}sort - sort the award
`
""")





    
bot.run(config.token)