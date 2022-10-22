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
from bot import utils


TOKEN = os.environ["DISCORD_TOKEN"]

VERSION = "v0.2.0"

utils.table_create()
log = utils.make_logger("bot", os.getenv("LOG_LEVEL", "INFO"))
log.info("Starting up")
log.debug(f"Using discord.py version: {discord.__version__} and Python version {sys.version[0:5]}")


COGS_DIR = "./bot/cogs"

description = (
    "This Discord bot that assists with the Competitive Cyber Club Discord\n"
    "If you experience any issues then please use the ?report feature.\n"
    f"Version: {VERSION}"
)


class CCC_Bot(commands.Bot):
    """Main class for running bot"""

    def __init__(self):
        super().__init__(command_prefix="?", intents=discord.Intents.all(), description=description)
        self.log = log
        self.uptime = datetime.utcnow()
        self.list_updated, self.school_list = "", None
        self.__version__ = VERSION
        self.daily_reporting = True
        self.description = (
            "This Discord bot that assists with the Competitive Cyber Club Discord\n"
            "If you experience any issues then please use the ?report feature.\n"
            f"Version: {self.__version__}"
        )

    async def on_ready(self):
        """
        On Ready

        Startup function which shows servers it has connected to
        """
        await utils.update_list(self, not os.path.exists("school_list.csv"))
        app_info = await self.application_info()
        await utils.insert("bot_admins", [app_info.owner.name, app_info.owner.id])
        admin_roles = await utils.select("keys", "value", "key", "admin_role")
        for admin_role in admin_roles:
            for guild in self.guilds:
                role = discord.utils.get(guild.roles, name=admin_role)
                if role is not None:
                    for admin in role.members:
                        await utils.insert("bot_admins", [admin.name, admin.id])
        await self.change_presence(
            activity=discord.Activity(name="?help", type=discord.ActivityType.playing)
        )
        # Load all python files in the cogs directory
        for extension in [
            f.replace(".py", "")
            for f in os.listdir(COGS_DIR)
            if os.path.isfile(os.path.join(COGS_DIR, f))
        ]:
            try:
                log.debug(f"Loading cog: cogs.{extension}")
                await self.load_extension(f"cogs.{extension}")
            except commands.ExtensionError as e:
                log.error(f"Failed to load extension {extension}. {e}")
        await self.change_presence(
            activity=discord.Activity(name="?help", type=discord.ActivityType.playing)
        )
        log.info("Bot is ready to go")


bot = CCC_Bot()
bot.run(TOKEN, reconnect=True)
