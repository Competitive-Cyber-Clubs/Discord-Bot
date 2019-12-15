"Main bot file"
import os
import logging
import sys
import random
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
import utils

load_dotenv()

GUILD = os.getenv('DISCORD_GUILD')
TOKEN = os.getenv('DISCORD_TOKEN')


utils.datahandler.create()
log = utils.make_logger("bot", logging.DEBUG)
log.info("Starting up")
log.debug("Using discord.py version: {} and Python version {}"
          .format(discord.__version__, sys.version[0:5]))


client = Bot(command_prefix="$")


@client.event
async def on_ready():
    "Startup which shows servers it has conencted to"
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    log.info(
        '{} is connected to the following guild: '
        '{}'.format(client.user, client.guilds[0].name)
    )
    await client.change_presence(activity=discord.Game(name='Here to help!'))


@client.command(name="ping",
                help="Testing command that returns pong",
                description="Pong")
async def ping(ctx):
    "Simple command that replies pong to ping"
    log.debug("{} has sent ping.".format(ctx.author.name))
    await ctx.send("pong")


@client.command(name="add-school",
                help="Creates a new school")
async def new_school(ctx, *args):
    "Creates school"
    log.debug(len(args))
    if len(args) < 2:
        await ctx.send("Error: The argument add-school "
                       "requires at least 2 arguments")
        return

    if len(args) < 3:
        color = int("0x%06x" % random.randint(0, 0xFFFFFF), 0)  # nosec
    else:
        if len(args[2]) == 6:
            color = f'0x{color}'
        elif len(args[2]) == 7:
            color = color.replace('#', '0x')
        else:
            color = args[2]
        try:
            color = int(args[2])
        except TypeError:
            await ctx.send("Error: Please submit your color as hex")

    data = [args[0],
            args[1],
            color,
            (ctx.author.name+ctx.author.discriminator)]
    status = utils.insert("Schools", data, log)
    log.debug(status)
    if status:
        await ctx.send("There was an error with creating the role.\n"
                       "Please reach out to a bot admin.")
        # raise discord.ClientException
        return

    await ctx.guild.create_role(name=args[0], color=discord.Color(color),
                                mentionable=True,
                                reason="Added by {}".format(ctx.author.name))
    await ctx.send(
        "School \"{}\" has been created in {} region with color of 0x{}"
        .format(args[0], args[1], color)
        )


client.run(TOKEN)
