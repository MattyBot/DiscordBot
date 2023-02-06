import os
import discord
import discord.ext.commands as commands
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure

TOKEN = os.environ['TOKEN']
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents = discord.Intents.all()

client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    print("{0.user} is now online!".format(client))

#these are going to be all the Pings for nowS
@client.event
async def on_message(message):
  client.process_commands(message)
  await client.process_commands(message)
  if message.author == client.user:
    return

  if message.content.startswith('!hello'):
    await message.channel.send('Hello there!')

  if message.content.startswith('!gamehours'):
    await message.channel.send('The game room hours are from 10am Monday  through Friday \nBUT sometimes our teams will be practicing on cerain Mondays,Tuesdays, Fridays and if they are, the Game Room would start wrapping up around 5:30 to prep for our teams from 6-8pm')

  if message.content.startswith('!location'):
    await message.channel.send('The USU Games Room is located in the lower level of the East Conference Center, across from the Student Recreation Center. \nFor more information visit the website \nhttps://www.csun.edu/src/games-room%27%27')

  if message.content.startswith('!help'):
    await message.channel.send('commands include \n!gamehours\n!location\n!hello')


@client.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx,*, member : discord.Member = None, reason=None):
  if member is None:
    await ctx.send("Please mention someone to ban")
  if reason is None:
    reason = "Reason was not specified"
  await ctx.send(f'{member.mention} is banned.')
  await member.ban(reason=reason)      # could use ctx.guild.ban(member, reason=reason) here, works the same way though.

@client.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def unban(ctx, member: discord.User = None, *, reason=None): 
  if reason is None:
    reason = f"{ctx.author.name}#{ctx.author.discriminator} did not provide any reason"
  if member is None:
    await ctx.send("Please write a ID#discriminator to unban")
  x = len(reason)   
  if x > 460: # 460 is the character limit of the reason in discord
    return await ctx.send('Reason must be less or equal to 460 characters')
  else:
    await ctx.guild.unban(member, reason=reason) 

@ban.error
async def ban_error(ctx, error): 
    if isinstance(error, commands.MemberNotFound):
      await ctx.send("No member was found with the given argument")
    elif isinstance(error, commands.BotMissingPermissions):
      await ctx.send("Bot is missing Ban Members permission(s) to run this command.")
    elif isinstance(error,commands.MissingPermissions):
      await ctx.send("You are missing Ban Members permission(s) to run this command.")

@unban.error
async def unban_error(ctx, error): 
    if isinstance(error, commands.MemberNotFound):
      await ctx.send("No member was found with the given argument")
    elif isinstance(error, commands.BotMissingPermissions):
      await ctx.send("Bot is missing Ban Members permission(s) to run this command.")
    elif isinstance(error,commands.MissingPermissions):
      await ctx.send("You are missing Ban Members permission(s) to run this command.")

client.run(TOKEN)