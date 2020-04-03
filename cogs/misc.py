"""Misc features cog for CCC Bot"""
import random
from datetime import datetime
import logging
from discord.ext import commands
import utils


class MiscCog(commands.Cog, name="Misc"):
    """MiscCog
    ---

    Cog that deal with misc features contains ping and contact-admin.

    Commands:
    ---
        `ping`: Testing command that will DM the user pong and then delete the ping message.
        `contact-admin`: Report command. When triggered it will ask the user for a reason then ping
                         all admins with the message. *Might need to be disabled for spam*

    Arguments:
    ---
        `bot` `discord.commands.Bot` -- The bot class that deals with all the commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("bot")

    @commands.command(name="ping",
                      help="Testing command that returns pong",
                      hidden=True)
    async def ping(self, ctx):
        """Ping
        ---

        Testing command that will message the author pong and delete the author's ping message.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        self.log.debug("{} has sent ping.".format(ctx.author.name))
        await ctx.author.send("pong")
        await ctx.message.delete()

    @commands.command(name="report",
                      aliases=["contact-admin"],
                      help="Reporting feature.")
    async def contact_admin(self, ctx, *, message: str):
        """Contact-Admin
        ---

        A reporting command. When triggered, user will be prompted for a reason. Message will then
        be sent to all bot admins.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        reports = await utils.fetch("reports", "id")
        reportID = random.randint(1, 32767)  # nosec
        while reportID in reports:
            self.log.debug("reportID had to be regenerated")
            reportID = random.randint(1, 32767)  # nosec
        await utils.insert("reports",
                           [reportID,
                            (ctx.author.name+ctx.author.discriminator),
                            ctx.author.id,
                            message,
                            datetime.utcnow()])
        channels = await utils.select("admin_channels", "id", "log", "f")
        for channel in channels:
            to_send = self.bot.get_channel(channel)
            if to_send is None:
                self.log.warning('No channel found for id {}'.format(channel))
            await to_send.send("{} submitted the report:\n> {}".format(ctx.author.name, message))
