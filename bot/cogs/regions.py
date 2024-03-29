"""Cog responsible for region management"""
import cyberjake
import discord
from discord.ext import commands
from bot import utils


class RegionCog(commands.Cog, name="Regions"):
    """Region Cog

    Cog that holds the region commands

    **Commands:**
        - `add-region`: Command that adds a region and its role to the regions' database.

        - `list-regions`: Commands that list all the regions available to join.

    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        """Cog Check

        cog_check is set for the whole cog. Which makes all the commands in health admin only.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :return: User is bot admin
        :rtype: bool
        """
        return await utils.check_admin(ctx)

    @commands.command(name="add-region", help="Adds regions")
    async def add_region(self, ctx: commands.Context, *, region: str) -> None:
        """Add region

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param region: Name of region to add
        :type region: str
        :return: None
        """
        is_role = discord.utils.get(ctx.guild.roles, name=region)
        if not is_role:
            added_region = await ctx.guild.create_role(
                name=region,
                mentionable=True,
                reason=f"Added by {ctx.author.name}",
            )
            status = await utils.insert("regions", [region, added_region.id])
        else:
            status = "error"
        if status == "error":
            await cyberjake.error_embed(ctx, "Error creating the region.")
        else:
            await cyberjake.make_embed(
                ctx, color="28b463", title=f"Region '{region}' has been created."
            )

    @commands.command(name="list-regions", help="Lists available regions.")
    async def list_region(self, ctx: commands.Context) -> None:
        """List regions

        Admin command that lists the regions. Only returns a list.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :return: None
        """
        regions = sorted(await utils.fetch("regions", "name"))
        formatted = ""
        for region in regions:
            formatted += f" - {region} \n"
        await cyberjake.make_embed(ctx, title="Available Regions:", description=formatted)


async def setup(bot):
    """Needed for extension loading"""
    await bot.add_cog(RegionCog(bot))
