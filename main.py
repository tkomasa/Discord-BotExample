# imports
import datetime
import discord
from discord.ext import commands
from dotenv import dotenv_values
import random

# retrieve token from .env file
env = dotenv_values(".env")
TOKEN = env['DISCORD_TOKEN']
GUILD = env['DISCORD_GUILD']

bot = commands.Bot(command_prefix='!')  # makes bot with prefix for calls


# on startup printout
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        '------------------ INFO ------------------\n'
        f'Bot: {bot.user}\n'
        'Status: Connected\n'
        f'Server: {guild.name}(id: {guild.id})\n'
        '------------------------------------------'
    )

'''----------------------------------------------------------------------------------------------------------'''


# new server member welcome dm
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Greetings {member.name}! Welcome to GUILD_NAME_HERE.\n'
        'Please read the rules and OTHER_INFO_HERE.\n'
        'As well as, please fill out the form below:\n'
        'LINK_HERE'
    )


# command for msg response example
# called with !example
@bot.command(name='example', help='Provides example for basic command calls.')
async def example_call(ctx):
    responses = [
        'This is where an info dump could be!',
        'These responses are randomized.',
        'Turtle-12 is my Supreme Creator.',
        'I am a bot. Hello!'
    ]

    response = random.choice(responses)
    await ctx.send(response)


# example of converted parameters within command
# call with '!roll_dice # #'
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


# command that checks role before running
# example based on 'Starfighter' vs 'Fleet Command' role
# must be enlisted to run
@bot.command(name='role_info', help='Provides info on your assigned branch.')
@commands.has_role('Enlisted')
async def role_info(ctx):
    if filter(lambda a: 'Starfighter' in a, ctx.author.roles):
        response = "You are in Starfighter and Enlisted."
        await ctx.send(response)
    elif filter(lambda a: 'Fleet Command' in a, ctx.author.roles):
        response = "You are in Fleet Command and Enlisted."
        await ctx.send(response)
    elif filter(lambda a: 'Enlisted' in a, ctx.author.roles):
        response = "You are Enlisted."
        await ctx.send(response)
    else:
        await ctx.send("You do not have a proper Role to give information on.")


'''@bot.command(name='raise_exception', help='Raises an error for testing reasons.')
async def raise_exception(ctx):
    await ctx.send("*Error raised.*")
    raise discord.DiscordException'''


'''----------------------------------------------------------------------------------------------------------'''


# error handlers
@bot.event
async def on_command_error(ctx, error, *args, **kwargs):
    with open('err.log', 'a') as f:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.send("*You do not have the Role to run this command.*")
            f.write(f"\nMissing Role(s) {datetime.datetime.now()}: Content:<<{ctx.message.content}>> Other Info:{ctx.message}")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("*Private messages.*")
            f.write(f"\nNo Private Message(s) {datetime.datetime.now()}: Content:<<{ctx.message.content}>> Other Info:{ctx.message}")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("*Command is missing an argument.*")
            f.write(f"\nMissing Required Argument(s) {datetime.datetime.now()}: Content:<<{ctx.message.content}>> Other Info:{ctx.message}")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("*This command is currently disabled. Please try again later.*")
            f.write(f"\nDisabled Command {datetime.datetime.now()}: Content:<<{ctx.message.content}>> Other Info:{ctx.message}")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("*You do not have the permissions to do this.*")
            f.write(f"\nCheck Failure {datetime.datetime.now()}: Content:<<{ctx.message.content}>> Other Info:{ctx.message}")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("*This command is not listed in my dictionary.*")
            f.write(f"\nCommand Not Found {datetime.datetime.now()}: Content:<<{ctx.message.content}>> Other Info:{ctx.message}")
        elif isinstance(error, discord.DiscordException):
            await ctx.send("*Error Occurred. Please contact my creator:* turtallius#8013")
            f.write(f"\nException Caught {datetime.datetime.now()}: Content:<<{ctx.message.content}>> Other Info:{ctx.message}")


def main():
    bot.run(TOKEN)  # runs the client using token from .env


if __name__ == "__main__":
    main()
