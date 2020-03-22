"Main bot file"
import os
import logging
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
import cogs
import utils


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_NAME = os.getenv('OWNER_NAME')
OWNER_ID = os.getenv('OWNER_ID')
log_level = os.getenv('LOG_LEVEL')
if not log_level:
    log_level = logging.INFO


utils.create()
log = utils.make_logger("bot", log_level)
log.info("Starting up")
log.debug("Using discord.py version: {} and Python version {}"
          .format(discord.__version__, sys.version[0:5]))


client = commands.Bot(command_prefix="$", owner_id=OWNER_ID)


@client.event
async def on_ready():
    "Startup which shows servers it has conencted to"

    log.info(
        '{} is connected to the following guild: '
        '{}'.format(client.user, client.guilds[0].name)
    )
    utils.insert("bot_admins", [OWNER_NAME, OWNER_ID], log)
    admin_role = discord.utils.get(client.guilds[0].roles, name="Admin")
    for admin in admin_role.members:
        utils.insert("bot_admins", [admin.name, admin.id], log)
    await client.change_presence(activity=discord.Activity(
        name='Here to help!', type=discord.ActivityType.playing))


client.add_cog(cogs.RegionCog(client, log))
client.add_cog(cogs.AdminCog(client, log))
client.add_cog(cogs.RankCog(client))
client.add_cog(cogs.MiscCog(client, log))
client.add_cog(cogs.EventsCog(client))
client.add_cog(cogs.SchoolCog(client, log))


@client.event
async def on_command_error(ctx, error):
    """Reports errors to users"""
    errorID = len(utils.fetch("errors", "id"))
    if isinstance(error, commands.errors.MissingRole) or isinstance(error, commands.errors.CheckFailure):  # noqa: E501 pylint: disable=line-too-long
        await ctx.send("You do not have the correct role for this command.")
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("That command is not valid. Please use `$help`.")
    elif isinstance(error, commands.errors.CommandError):
        errorID = len(utils.fetch("errors", "id"))
        log.error((errorID, error))
        await ctx.send("There was a command error.\n"
                       "Please report it for investgation.\n"
                       "Error #{}".format(errorID))
        utils.insert("errors", [errorID, str(error)], log)
    else:
        errorID = len(utils.fetch("errors", "id"))
        log.error((errorID, error))
        await ctx.send("There was an unknown error.\n"
                       "Please report it for investigation.\n"
                       "Error #{}".format(errorID))
        log.error("There was the following error: {}".format(error))

client.run(TOKEN)
