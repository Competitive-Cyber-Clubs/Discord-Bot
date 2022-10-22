"""Rank features cog for CCC Bot"""
import discord.utils
from discord.ext import commands
from bot.utils import make_embed, error_message


class RankCog(commands.Cog, name="Rank"):
    """Rank Cog
    Cog that deals with rank commands

    **Commands:**
        - `add-rank`: Command that add either student, alumni, or professor role.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add-rank", help="Assigns student, alumni or professor role.")
    @commands.has_role("verified")
    async def add_rank(self, ctx: commands.Context, *, rank: str) -> None:
        """Add Rank

        Allows users to set student, alumni or professor role.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param rank: Name of rank to add
        :type rank: str
        :return: None
        """
        user = ctx.message.author
        ranks = ["student", "professor", "alumni"]
        checked = [i for i in user.roles if i.name.lower() in ranks]
        if len(checked) > 0:
            await error_message(ctx, "You already have a rank.")
        else:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=rank))
            await make_embed(
                ctx,
                color="28b463",
                title="Success",
                description="Rank assigned successfully",
            )


async def setup(bot):
    """Needed for extension loading"""
    await bot.add_cog(RankCog(bot))
