"""Misc features cog for CCC Bot"""
from discord.ext import commands


class MiscCog(commands.Cog, name="Misc"):
    """Commands that deal with misc features"""
    def __init__(self, bot, log):
        self.bot = bot
        self.log = log

    @commands.command(name="ping",
                      help="Testing command that returns pong",
                      description="Pong")
    async def ping(self, ctx):
        "Simple command that replies pong to ping"
        self.log.debug("{} has sent ping.".format(ctx.author.name))
        await ctx.author.send("pong")
        await ctx.message.delete()
