"""Rank features cog for CCC Bot"""
import discord
from discord.ext import commands


class RankCog(commands.Cog, name="Rank"):
    """Cog that deals with rank commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add-rank",
                      help="Adds student, alumni or professor role.")
    @commands.has_role("verified")
    async def addrank(self, ctx, rank):
        """Allows users to set student, alumni or professor role."""
        user = ctx.message.author
        ranks = ["student", "professor", "alumni"]
        checked = [i for i in user.roles if i.name.lower() in ranks]
        if len(checked) > 0:
            await ctx.send("Error: You already have a rank.")
            return
        rank = discord.utils.get(ctx.guild.roles, name=rank)
        await user.add_roles(rank)
        await ctx.send("Rank assigned successfully")
