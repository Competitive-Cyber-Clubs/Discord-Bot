"""Cog responsible for region management"""
import discord
from discord.ext import commands
import utils


class RegionCog(commands.Cog, name="Regions"):
    """RegionCog
    ---

    Cog that holds the region commands

    Commands:
    ---
        `add-region`: Command that adds a region and its role to to the regions database.
        `list-regions`: Commands that list all the regions available to join.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        """cog_check
        ---

        cog_check is set for the whole cog. Which makes all the commands in health admin only.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.

        Returns:
            bool -- True if the user in the bot admins
        """
        return await utils.check_admin(ctx)

    @commands.command(name="add-region", help="Adds regions")
    async def add_region(self, ctx: commands.Context, *, region: str):
        """Add_region
        ---

        Allows admins to add regions.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            region {str} -- Name of region to add.
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
            await utils.error_message(ctx, "Error creating the region.")
        else:
            await utils.make_embed(ctx, color="28b463", title="Region has been created.")

    @commands.command(name="list-regions", help="Lists available regions.")
    async def list_region(self, ctx: commands.Context):
        """list-regions
        ---

        Admin command to lists the regions. Only returns a list.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        regions = sorted(await utils.fetch("regions", "name"))
        formatted = ""
        for region in regions:
            formatted += " - {} \n".format(region)
        await utils.make_embed(ctx, title="Available Regions:", description=formatted)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(RegionCog(bot))
