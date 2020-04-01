"Main bot file"
import os
import sys
from datetime import datetime
import secrets
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
    log_level = "INFO"


utils.table_create()
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
    log.debug(client.guilds)
    await utils.insert("bot_admins", [OWNER_NAME, OWNER_ID])
    admin_roles = await utils.select("keys", "value", "key", "admin_role")
    for admin_role in admin_roles:
        role = discord.utils.get(client.guilds[0].roles,
                                 name=admin_role)
        for admin in role.members:
            await utils.insert("bot_admins", [admin.name, admin.id])
    await client.change_presence(activity=discord.Activity(
        name='Here to help!', type=discord.ActivityType.playing))


cogs_list = [cogs.RegionCog(client),
             cogs.AdminCog(client),
             cogs.MiscCog(client),
             cogs.SchoolCog(client),
             cogs.HealthCog(client),
             cogs.RankCog(client),
             cogs.EventsCog(client)
             ]
for cog in cogs_list:
    client.add_cog(cog)


@client.event
async def on_command_error(ctx, error):
    """Reports errors to users"""
    if isinstance(error, (commands.errors.MissingRole, commands.errors.CheckFailure)):
        await ctx.send("You do not have the correct role for this command.")
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("{} is not valid.\nPlease use `$help` to find valid commands.".format(
            ctx.message.content))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("`{}` has missing required arguments".format(ctx.message.content))
    elif isinstance(error, commands.errors.CommandError):
        errors = await utils.fetch("errors", "id")
        errorID = secrets.SystemRandom().randint(1, 32767)
        while errorID in errors:
            errorID = secrets.SystemRandom().randint(1, 32767)
        log.error((errorID, error))
        await ctx.send("There was a command error.\n"
                       "Please report it for investgation.\n"
                       "Error #{}".format(errorID))
        await utils.insert("errors", [
            errorID, ctx.message, ctx.command, str(error), datetime.utcnow()]
                          )
    else:
        log.error((errorID, error))
        await ctx.send("There was an unknown error.\n"
                       "Please report it for investigation.\n"
                       "Error #{}".format(errorID))
        log.error("There was the following error: {}".format(error))
        await utils.insert("errors", [
            errorID, ctx.message, ctx.command, str(error), datetime.utcnow()]
                          )

client.run(TOKEN, reconnect=True)
