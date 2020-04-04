"""Cog the preforms health functions"""
from datetime import datetime
import logging
from discord.ext import commands
import discord
import utils


class HealthCog(commands.Cog, name="Health"):
    """HealthCog
    ---

    Cog that holds the health commands and is responsible for updating the
    tables when roles change in discord.

    Commands:
    ---
        `check-health`: Makes sure that all the roles in the tables `schools` and `regions` map
             to roles in the discord server.

    Events:
    ---
        `on_guild_role_update`: Event that is triggered when a role is updated.

        `on_guild_role_delete`: Event that is triggered when a role is deleted.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("bot")

    async def cog_check(self, ctx):
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

    @commands.command(name="check-health",
                      help="Checks health of roles for schools and regions")
    async def check_health(self, ctx):
        """check-health
        ---

        Checks health of roles for schools and regions. It pulls all the IDs for school and
        region roles. Then compares the names of the matching ids to see if they match. If
        they match then added to a list called success and if the check fails then then
        both names are added to a list called fail.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.

        """
        async with ctx.typing():
            table_schools = await utils.fetch("schools", "school")
            regions = await utils.fetch("regions", "name")
            success, fail = [], []
            for roles in [table_schools, regions]:
                for role in roles:
                    try:
                        role_name = discord.utils.get(ctx.guild.roles, name=role).name
                        if role_name == role:
                            success.append(role_name)
                        else:
                            fail.append((role_name, role))
                    except AttributeError:
                        self.log.error("Attribute error with role {}".format(role_name))
                        fail.append((role, None))
        await ctx.send("Check complete.\nThere were {} successes and {} failures".format(
            len(success), len(fail)))

    @commands.command(name="get-x", help="Gets all errors or reports for the day.")
    async def error_report(self, ctx: commands.Context, which: str):
        """error_report
        ---

        Gets all the errors for the same day.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            which {str} --- which item to get, reports or errors.
        """
        if which == "errors":
            columns = "id, message, command, error"
        elif which == "reports":
            columns = "name, message"
        else:
            return await ctx.send("Please pick a valid option.")
        date = datetime.utcnow().strftime("%Y-%m-%d")
        results = await utils.select(which,
                                     columns,
                                     "date_trunc('day', time)",
                                     date)
        if not results:
            await ctx.send("No {} for {}".format(which, date))
        else:
            await utils.list_message(ctx, results, which)

    @commands.command(name="test-log")
    async def check_log(self, ctx):
        """test-log
        ---

        Tests to makesure that that logging feature works.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        await utils.admin_log(self.bot, "Test-log", True)
        await utils.admin_log(self.bot, 'Test-log', False)
        await ctx.send("Test Complete")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        """on_guild_role_update
        ---

        Runs when a role is edited. Logs the old name and new name then updates the name in the
        table.

        Arguments:
        ---
            before {discord.Role} -- The discord role before it was edited.
            after {discord.Role} -- The discord role after it was edited.
        """
        self.log.info("Old role {} now new role {}".format(before, after))
        await utils.update("schools", "school", before.name, after.name)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        """on_guild_role_delete
        ---

        Runs when a role is deleted. Will only delete an entry if it existed in the schools or
        regions table.

        Arguments:
        ---
            role {discord.Role} -- The role that was deleted.
        """
        managed = False
        for table in ["schools", "regions"]:
            if await utils.select(table, "id", "id", role.id):
                await utils.delete("schools", "id", role.id)
                self.log.warning("Role \"{}\" was deleted. It was in {}".format(role.name, table))
                managed = True
        if not managed:
            self.log.info("Role \"{}\" was deleted. It was not a managed role".format(role.name))

        await utils.admin_log(self.bot, "Role: {} was deleted".format(role.name), True)
