"""Rank features cog for CCC Bot"""
import discord.utils
from discord.ext import commands
from utils import make_embed


class RankCog(commands.Cog, name="Rank"):
    """RankCog
    ---

    Cog that deals with rank commands

    Commands:
    ---
        `add-rank`: Command that add either student, alumni, or professor role.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add-rank",
                      help="Assigns student, alumni or professor role.")
    @commands.has_role("verified")
    async def add_rank(self, ctx, *, rank: str):
        """Add_Rank
        ---

        Allows users to set student, alumni or professor role.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            rank {str} -- name of rank to add.
        """
        user = ctx.message.author
        ranks = ["student", "professor", "alumni"]
        checked = [i for i in user.roles if i.name.lower() in ranks]
        if len(checked) > 0:
            await make_embed(ctx, "FF0000", title="Error: You already have a rank.")
        else:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=rank))
            await make_embed(ctx, color="28b463", title="Success",
                             description="Rank assigned successfully")


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(RankCog(bot))
