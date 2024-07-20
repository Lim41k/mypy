
TOCKEN = 'your tocken'

# This example requires the 'message_content' intent.

import discord

from discord.ext import commands

# intents = discord.Intents.default()
# intents.message_content = True # if  - server message
# intents.members = True # if  - person message
intents = discord.Intents().all()
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command(name="tt")
async def test(ctx, arg):
    print(ctx)
    await ctx.send(f'You passed {arg}')

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Пожалуйста, укажите пользователя.")
        return
    
    embed = discord.Embed(title="Информация о пользователе", color=0x00ff00)
   
    embed.add_field(name="Имя пользователя", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Дата присоединения", value=member.joined_at, inline=True)
    embed.add_field(name="Роли", value=", ".join([role.name for role in member.roles if role.name != "@everyone"]), inline=True)
    # embed.set_thumbnail(url=member.avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def list_members(ctx):
    if ctx.guild is None:
        await ctx.send("Эта команда может быть использована только на сервере.")
        return
    print(ctx)
    members = ctx.guild.members
    member_list = "\n".join([member.name for member in members])
    
    # Ограничение на длину сообщения в Discord (2000 символов)
    if len(member_list) > 2000:
        await ctx.send("Список пользователей слишком длинный, чтобы отобразить его в одном сообщении.")
    else:
        await ctx.send(f"Список пользователей сервера:\n{member_list}")


# @bot.event
# async def on_message(message):

#     print(message)
#     print(message.author, message.content)
#     if message.author == bot.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')


bot.run(TOCKEN)
