"""Cogs the preforms admin contact functions"""
import asyncio
from discord.ext import commands
import utils


class ContactCog(commands.Cog, name="Contact"):
    """Cog that holds the health commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="contact-admin",
                      aliases=["report"],
                      help="Contacts a bot admin")
    async def coadmin(self, ctx):
        """Will contact a bot admin"""
        await ctx.send("What is the issue that you want the admin to respond to.")
        try:
            msg = await self.bot.wait_for('message', timeout=300)
        except asyncio.TimeoutError:
            ctx.send("Took to long. You have 300 seconds to send a response.")
            return
        results = utils.fetch("bot_admins", "id")
        bot_admins = [x for x in results if x != self.bot.user.id]
        for admin in bot_admins:
            user = self.bot.get_user(admin)
            await user.send("{} send the report:\n{}".format(msg.author, msg.content))
