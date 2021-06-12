"""Misc features cog for CCC Bot"""
import random
from datetime import datetime
import logging
from discord.ext import commands
from bot import utils

log = logging.getLogger("bot")


class MiscCog(commands.Cog, name="Misc"):
    """MiscCog
    ---

    Cog that deal with misc features contains ping, report and uptime.

    Commands:
    ---
        `ping`: Testing command that will DM the user pong and then delete the ping message.
        `report`: Report command. When triggered it will ask the user for a reason then ping
                         all admins with the message. *Might need to be disabled for spam*
        `uptime`: Lists uptime for bot and when it was started.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Testing command that returns pong", hidden=True)
    async def ping(self, ctx: commands.Context):
        """Ping
        ---

        Testing command that will message the author pong and delete the author's ping message.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        log.debug("{} has sent ping.".format(ctx.author.name))
        await ctx.message.delete()
        embed = await utils.make_embed(ctx, send=False, title="PONG")
        url = "https://peterfrezzini.com/content/images/2016/12/pong_logo.jpg"
        embed.set_image(url=url)
        embed.set_footer(text="Image from https://peterfrezzini.com/pong-game-cover/")
        await ctx.author.send(embed=embed)

    @commands.command(name="uptime", help="Gets uptime of bot")
    async def Uptime(self, ctx: commands.Context):
        """uptime
        ---

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        uptime = datetime.utcnow() - self.bot.uptime
        uptime = ":clock1: Days: {}, Hours: {}, Minutes: {}, Seconds: {}".format(
            uptime.days,
            uptime.seconds // 3600,  # Hours
            (uptime.seconds // 60) % 60,  # Minutes
            uptime.seconds % 60,  # Seconds
        )

        start_time = self.bot.uptime.strftime("%Y-%m-%d %H:%M")
        list_string_time = self.bot.list_updated.strftime("%Y-%m-%d %H:%M")
        description = "Bot has been online since {} UTC\n School list last updated {}".format(
            start_time, list_string_time
        )

        await utils.make_embed(
            ctx, title=uptime, description=description, footer=self.bot.__version__
        )

    @commands.command(
        name="report",
        aliases=["contact-admin"],
        help="Reporting feature.\n"
        "Use if you are experiencing issues with the bot or in the server.",
    )
    async def contact_admin(self, ctx: commands.Context, *, message: str):
        """Contact-Admin
        ---

        A reporting command. When triggered, user will be prompted for a reason. Message will then
        be sent to all bot admins.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        reports = await utils.fetch("reports", "id")
        report_id = random.randint(1, 32767)  # nosec
        while report_id in reports:
            log.warning("report_id had to be regenerated")
            report_id = random.randint(1, 32767)  # nosec
        await utils.insert(
            "reports",
            [
                report_id,
                (ctx.author.name + ctx.author.discriminator),
                ctx.author.id,
                message,
                datetime.utcnow(),
            ],
        )
        channels = await utils.select("admin_channels", "id", "log", "f")
        for channel in channels:
            to_send = self.bot.get_channel(channel)
            if to_send is None:
                log.warning("No channel found for id {}".format(channel))
            await utils.make_embed(
                ctx,
                title="New Report",
                description="{} submitted the report:\n> {}".format(ctx.author.name, message),
            )

        response_msg = (
            "The admins have received your report.\nThey will investigation and may reach out"
        )
        await utils.make_embed(ctx, title="Report Received", description=response_msg)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(MiscCog(bot))
