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
                      help="Checks health of roles for schools and regions")
    @commands.check(utils.check_admin)
    async def chealth(self, ctx):
        """Checks health of roles for schools and regions"""
        table_schools = utils.fetch("schools", "school")
        regions = utils.fetch("regions", "name")
        success, fails = [], []
        async with ctx.typing():
            for roles in [table_schools, regions]:
                for role in roles:
                    try:
                        role_name = discord.utils.get(ctx.guild.roles, name=role).name
                        if role_name == role:
                            success.append(role_name)
                        else:
                            fails.append((role_name, role))
                    except AttributeError:
                        self.log.error("Attribute error with role {}".format(role_name))
                        fails.append((role, None))
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
        self.log.warning("The role \"{}\" was deleted".format(role.name))
