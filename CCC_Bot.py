
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
---
LOG_LEVEL {DEFAULT: INFO}:
"""
import os
import sys
from datetime import datetime
from discord.ext import commands
import discord
from dotenv import load_dotenv
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


initial_extensions = [
    'cogs.admin',
    'cogs.errors',
    'cogs.events',
    'cogs.health',
    'cogs.misc',
    'cogs.rank',
    'cogs.regions',
    'cogs.schools',
    'cogs.search',
    'cogs.tasks']

description = ("The Discord bot that assists with the Competitive Cyber Club Discord\n"
               "If you experience any issues then please use the $report feature.")


class CCC_Bot(commands.Bot):  # pylint: disable=missing-class-docstring
    def __init__(self):
        super().__init__(command_prefix="$",
                         owner_id=OWNER_ID,
                         description=description)

        self.uptime = datetime.utcnow()
        self.__version__ = "beta"

    async def on_ready(self):
        "Startup which shows servers it has conencted to"
        log.info(
            '{} is connected to the following guild: '
            '{}'.format(self.user, self.guilds[0].name)
        )
        await utils.insert("bot_admins", [OWNER_NAME, int(OWNER_ID)])
        admin_roles = await utils.select("keys", "value", "key", "admin_role")
        for admin_role in admin_roles:
            role = discord.utils.get(self.guilds[0].roles,
                                     name=admin_role)
            for admin in role.members:
                await utils.insert("bot_admins", [admin.name, admin.id])
        await self.change_presence(activity=discord.Activity(
            name='Here to help!', type=discord.ActivityType.playing))
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except commands.ExtensionError as e:
                log.error('Failed to load extension {}. {}'.format(extension, e))


bot = CCC_Bot()
bot.run(TOKEN, reconnect=True)
