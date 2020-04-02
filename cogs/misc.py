"""Misc features cog for CCC Bot"""
import asyncio
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

    @commands.command(name="contact-admin",
                      aliases=["report"],
                      help="Contacts a bot admin")
    async def contact_admin(self, ctx):
        """Contact-Admin
        ---

        A reporting command. When triggered, user will be prompted for a reason. Message will then
        be sent to all bot admins.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        await ctx.send("What is the issue that you want the admin to respond to.")
        try:
            msg = await self.bot.wait_for('message', timeout=300)
        except asyncio.TimeoutError:
            ctx.send("Took to long. You have 300 seconds to send a response.")
            return
        channels = await utils.select("admin_channels", "id", "log", "f")[0]
        for channel in channels:
            to_send = self.bot.get_channel(channel)
            await to_send.send("{} send the report:\n> {}".format(msg.author, msg.content))
