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
        `bot` `discord.commands.Bot` -- The bot class that deals with all the commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add-region",
                      help="Adds regions")
    @commands.check(utils.check_admin)
    async def add_region(self, ctx, *, region: str):
        """Add_region
        ---

        Allows admins to add regions.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            region {str} -- name of region to add.
        """
        is_role = discord.utils.get(ctx.guild.roles, name=region)
        if not is_role:
            added_region = await ctx.guild.create_role(name=region,
                                                       mentionable=True,
                                                       reason="Added by {}".format(ctx.author.name))
        status = await utils.insert("regions", [region, added_region.id])
        if status != "error":
            await ctx.send('Region has been created.')
        else:
            await ctx.send("There was an error creating the region.")

    @commands.command(name="list-regions",
                      help="Lists available regions.")
    @commands.check(utils.check_admin)
    async def listregion(self, ctx):
        """list-regions
        ---

        Admin command to lists the regions. Only returns a list.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        regions = await utils.fetch("regions", "name")
        formated = "Available Regions:\n"
        for region in regions:
            formated += " - {} \n".format(region)
        await ctx.send(formated)
