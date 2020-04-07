
"""CCC Bot
---
Discord Bot for Competitive Cyber Clubs Server.

All values are loaded from environment variables. Also can be loaded from a .env file.
Required Variables:
---
DISCORD_TOKEN: The token for the bot.
OWNER_NAME: The username of the bot owner
OWNER_ID: The Discord ID of the bot owner

Optional:
LOG_LEVEL {DEFAULT: INFO}:
"""
import os
import sys
from datetime import datetime
import random
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


bot = commands.Bot(command_prefix="$", owner_id=OWNER_ID)


@bot.event
async def on_ready():
    "Startup which shows servers it has conencted to"
    log.info(
        '{} is connected to the following guild: '
        '{}'.format(bot.user, bot.guilds[0].name)
    )
    await utils.insert("bot_admins", [OWNER_NAME, int(OWNER_ID)])
    admin_roles = await utils.select("keys", "value", "key", "admin_role")
    for admin_role in admin_roles:
        role = discord.utils.get(bot.guilds[0].roles,
                                 name=admin_role)
        for admin in role.members:
            await utils.insert("bot_admins", [admin.name, admin.id])
    await bot.change_presence(activity=discord.Activity(
        name='Here to help!', type=discord.ActivityType.playing))
    # TaskCog added here because it needs to be able to find channels.
    bot.add_cog(cogs.TaskCog(bot))


cogs_list = [cogs.RegionCog(bot),
             cogs.AdminCog(bot),
             cogs.MiscCog(bot),
             cogs.SchoolCog(bot),
             cogs.HealthCog(bot),
             cogs.RankCog(bot),
             cogs.EventsCog(bot),
             cogs.SearchCog(bot)
             ]
for cog in cogs_list:
    bot.add_cog(cog)


@bot.event
async def on_command_error(ctx, error):
    """Reports errors to users"""
    if isinstance(error, (commands.errors.MissingRole, commands.errors.CheckFailure)):
        error_msg = "You do not have the correct role for this command."
        embed = await utils.make_embed(ctx, "FF0000", title="Error:",
                                       description=error_msg)
    elif isinstance(error, commands.errors.CommandNotFound):
        error_msg = "{} is not valid.\nPlease use `$help` to find valid commands.".format(
            ctx.message.content)
    elif isinstance(error, commands.MissingRequiredArgument):
        error_msg = "`{}` has missing required arguments".format(ctx.message.content)
    elif isinstance(error, commands.errors.CommandError):
        errors = await utils.fetch("errors", "id")
        errorID = random.randint(1, 32767)  # nosec
        while errorID in errors:
            log.debug("Error ID had to be regenerated")
            errorID = random.randint(1, 32767)  # nosec

        error_info = [
            errorID,
            ctx.message.content,
            "COG: {} COMMAND: {}".format(ctx.command.cog.qualified_name, ctx.command.name),
            str(error),
            datetime.utcnow()]

        log.error(error_info)
        error_msg = ("There was a command error.\n"
                     "Please report it for investgation.\n"
                     "Error #{}".format(errorID))
        await utils.insert("errors", error_info)
    else:
        errors = await utils.fetch("errors", "id")
        errorID = random.randint(1, 32767)  # nosec
        while errorID in errors:
            log.debug("Error ID had to be regenerated")
            errorID = random.randint(1, 32767)  # nosec

        log.error((errorID, error))
        error_msg = ("There was an unknown error.\n"
                     "Please report it for investigation.\n"
                     "Error #{}".format(errorID))
        log.error("There was the following error: {}".format(error))
        await utils.insert("errors", error_info)

    embed = await utils.make_embed(ctx, "FF0000", title="Error:",
                                   description=error_msg)
    await ctx.send(embed=embed)

bot.run(TOKEN, reconnect=True)
