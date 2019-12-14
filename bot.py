import os
import discord
import logging
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
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    log.info(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}'
    )
    await client.change_presence(activity=discord.Game(name='Here to help!'))


@client.command(name="ping",
                help="Testing command that returns pong",
                description="Pong")
async def ping(ctx):
    log.debug("{0} has sent ping.".format(ctx.author))
    await ctx.send("pong")

client.run(TOKEN)
