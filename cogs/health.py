"""Cogs the preforms health functions"""
from discord.ext import commands
import discord
import utils


class HealthCog(commands.Cog, name="Health"):
    """Cog that holds the health commands"""
    def __init__(self, bot, log):
        self.bot = bot
        self.log = log

    @commands.command(name="check-health",
                      help="Checks health of table")
    @commands.check(utils.check_admin)
    async def chealth(self, ctx):
        """Checks health of roles"""
        table_schools = utils.fetch("schools", "id, school")
        success, fails = [], []
        async with ctx.typing():
            for school in table_schools:
                school_name = discord.utils.get(ctx.guild.roles, id=school[0]).name
                if school_name == school[1]:
                    success.append(school_name)
                else:
                    fails.append((school_name, school[1]))
        await ctx.send("Check complete.\nThere were {} successes and {} failures".format(
            len(success), len(fails)))

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """Runs when a role is renamed"""
        self.log.info("Old role {} now new role {}".format(before, after))
        utils.update("schools", "school", before.name, after.name)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Runs when a role is delete.
           Will only delete an entry if it existed in the schools table."""
        utils.delete("schools", "id", role.id)
        self.log.warning("The role {} was deleted".format(role.name))
