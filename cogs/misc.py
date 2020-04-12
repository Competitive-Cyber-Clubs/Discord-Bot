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
        bot {discord.commands.Bot} -- The bot
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
        await ctx.message.delete()
        embed = await utils.make_embed(ctx, send=False, title="PONG")
        url = "https://peterfrezzini.com/content/images/2016/12/pong_logo.jpg"
        embed.set_image(url=url)
        embed.set_footer(text="Image from https://peterfrezzini.com/pong-game-cover/s")
        await ctx.author.send(embed=embed)

    @commands.command(name="uptime",
                      help="Gets uptime of bot")
    async def uptime(self, ctx):
        """uptime
        ---

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        current_time = datetime.utcnow()

        uptime = current_time - self.bot.uptime
        uptime = "Days: {}, Hours: {}, Minutes: {}, Seconds: {}".format(uptime.days,
                                                                        uptime.seconds // 3600,
                                                                        uptime.seconds // 60,
                                                                        uptime.seconds % 60)
        start_time = self.bot.uptime.strftime("%Y-%m-%d %H:%M")
        description = "Bot has been online since {} UTC".format(start_time)
        await utils.make_embed(ctx, title=uptime,
                               description=description)

    @commands.command(name="report",
                      aliases=["contact-admin"],
                      help="Reporting feature.\n"
                           "Use if you are experaincing issues with the bot or in the server.")
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
            await utils.make_embed(ctx, title="New Report",
                                   description="{} submitted the report:\n> {}"
                                   .format(ctx.author.name, message))

        respone_msg = ("The admins have received your report.\n"
                       "They will investigation and may reach out")
        await utils.make_embed(ctx, title="Report Received",
                               description=respone_msg)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(MiscCog(bot))
