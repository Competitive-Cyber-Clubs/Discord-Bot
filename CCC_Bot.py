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
import utils


TOKEN = os.environ["DISCORD_TOKEN"]
OWNER_NAME = os.environ["OWNER_NAME"]
OWNER_ID = os.environ["OWNER_ID"]


utils.table_create()
log = utils.make_logger("bot", os.getenv("LOG_LEVEL", "INFO"))
log.info("Starting up")
log.debug(
    "Using discord.py version: {} and Python version {}".format(
        discord.__version__, sys.version[0:5]
    )
)

initial_extensions = [
    "cogs.admin",
    "cogs.errors",
    "cogs.events",
    "cogs.health",
    "cogs.misc",
    "cogs.rank",
    "cogs.regions",
    "cogs.schools",
    "cogs.search",
    "cogs.tasks",
]


class CCC_Bot(commands.Bot):  # pylint: disable=missing-class-docstring
    def __init__(self):
        super().__init__(
            command_prefix=("$", "?"), owner_id=OWNER_ID, intents=discord.Intents.all()
        )

        self.uptime = datetime.utcnow()
        self.list_updated, self.school_list = "", ""
        self.__version__ = "v0.1.1"
        self.description = (
            "This Discord bot that assists with the Competitive Cyber Club Discord\n"
            "If you experience any issues then please use the ?report feature.\n"
            f"Version: {self.__version__}"
        )

    async def on_ready(self):
        """Startup which shows servers it has connected to"""
        await utils.update_list(self, not os.path.exists("school_list.csv"))
        log.info("{} is connected to the following guilds: " "{}".format(self.user, self.guilds))
        await utils.insert("bot_admins", [OWNER_NAME, int(OWNER_ID)])
        admin_roles = await utils.select("keys", "value", "key", "admin_role")
        for admin_role in admin_roles:
            role = discord.utils.get(self.guilds[0].roles, name=admin_role)
            if role is not None:
                for admin in role.members:
                    await utils.insert("bot_admins", [admin.name, admin.id])
        await self.change_presence(
            activity=discord.Activity(name="?help", type=discord.ActivityType.playing)
        )
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except commands.ExtensionError as e:
                log.error("Failed to load extension {}. {}".format(extension, e))


bot = CCC_Bot()
bot.run(TOKEN, reconnect=True)
