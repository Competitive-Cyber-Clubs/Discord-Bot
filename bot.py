"Main bot file"
import os
import logging
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
import utils

load_dotenv()

utils.datahandler.create()
log = utils.make_logger("bot", logging.DEBUG)
log.info("Starting up")

GUILD = os.getenv('DISCORD_GUILD')
TOKEN = os.getenv('DISCORD_TOKEN')

BOT_PREFIX = ("$", "!")


client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    "Startup which shows servers it has conencted to"
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    log.info(
        '{user} is connected to the following guild:\n'
        '{guild}', user=client.user, guild=client.guilds
    )
    await client.change_presence(activity=discord.Game(name='Here to help!'))


@client.command(name="ping",
                help="Testing command that returns pong",
                description="Pong")
async def ping(ctx):
    "Simple command that replies pong to ping"
    log.debug("{0} has sent ping.", ctx.author)
    await ctx.send("pong")

client.run(TOKEN)
