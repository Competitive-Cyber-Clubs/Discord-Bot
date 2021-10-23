"""Misc features cog for CCC Bot"""
import random
from datetime import datetime
from discord.ext import commands
from bot import utils


class MiscCog(commands.Cog, name="Misc"):
    """Misc Cog

    Cog that deal with misc features contains ping, report and uptime.

    **Commands:**
        - `ping`: Testing command that will DM the member pong and then delete the ping message.

        - `report`: Report command. When triggered it will ask the member for a reason then ping
                    all admins with the message. *Might need to be disabled for spam*

        - `uptime`: Lists uptime for bot and when it was started.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Testing command that returns pong", hidden=True)
    async def ping(self, ctx: commands.Context) -> None:
        """Ping

        Testing command that will message the author pong and delete the author's ping message.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :return: None
        """
        self.bot.log.debug(f"{ctx.author.name} has sent ping.")
        await ctx.message.delete()
        embed = await utils.make_embed(ctx, send=False, title="PONG")
        url = "https://peterfrezzini.com/content/images/2016/12/pong_logo.jpg"
        embed.set_image(url=url)
        embed.set_footer(text="Image from https://peterfrezzini.com/pong-game-cover/")
        await ctx.author.send(embed=embed)

    @commands.command(name="uptime", help="Gets uptime of bot")
    async def uptime(self, ctx: commands.Context) -> None:
        """
        Uptime

        Command that shows how long the bot has been online

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :return: None
        """
        uptime = datetime.utcnow() - self.bot.uptime

        uptime = (
            ":clock1: Days: {}, Hours: {}, Minutes:{}, Seconds: {}".format(  # pylint: disable=C0209
                uptime.days,
                uptime.seconds // 3600,  # Hours
                (uptime.seconds // 60) % 60,  # Minutes
                uptime.seconds % 60,  # Seconds
            )
        )

        start_time = self.bot.uptime.strftime("%Y-%m-%d %H:%M")
        list_string_time = self.bot.list_updated.strftime("%Y-%m-%d %H:%M")
        description = (
            f"Bot has been online since {start_time} UTC\n "
            f"School list last updated {list_string_time}"
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
    async def report(self, ctx: commands.Context, *, message: str) -> None:
        """Report

        reporting command. When triggered, member will be prompted for a reason. Message will then
        be sent to all bot admins.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param message: Report message sent
        :type message: str
        :return: None
        """
        reports = await utils.fetch("reports", "id")
        report_id = random.randint(1, 32767)  # nosec
        while report_id in reports:
            self.bot.log.warning("report_id had to be regenerated")
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
                self.bot.log.warning(f"No channel found for id channel {channel}")
            await utils.make_embed(
                ctx,
                title="New Report",
                description=f"{ctx.author.name} submitted the report:\n> {message}",
            )

        response_msg = (
            "The admins have received your report.\nThey will investigation and may reach out"
        )
        await utils.make_embed(ctx, title="Report Received", description=response_msg)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(MiscCog(bot))
