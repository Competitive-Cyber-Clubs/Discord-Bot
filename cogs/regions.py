"""Cog responsible for region management"""
import discord
from discord.ext import commands
import utils


class RegionCog(commands.Cog, name="Regions"):
    """Cog that holds the region commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add-region",
                      help="Adds regions")
    @commands.check(utils.check_admin)
    async def addregion(self, ctx, region):
        """Allows admins to add regions"""
        is_role = discord.utils.get(ctx.guild.roles, name=region)
        if not is_role:
            await ctx.guild.create_role(name=region,
                                        mentionable=True,
                                        reason="Added by {}".format(ctx.author.name))
        status = utils.insert("regions", [region])
        if not status == "error":
            await ctx.send('Region has been created.')
        else:
            await ctx.send("There was an error creating the region.")

    @commands.command(name="list-regions",
                      help="Lists available regions.")
    @commands.check(utils.check_admin)
    async def listregion(self, ctx):
        """Admin command to lists the regions"""
        regions = utils.fetch("regions", "name")
        formated = "Available Regions:\n"
        for item in regions:
            formated += item + "\n"
        await ctx.send(formated)
