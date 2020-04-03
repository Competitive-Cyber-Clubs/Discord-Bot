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
        `bot` `discord.commands.Bot` -- The bot class that deals with all the commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("bot")

    @commands.command(name="check-health",
                      help="Checks health of roles for schools and regions")
    @commands.check(utils.check_admin)
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

    @commands.command(name="get-errors", help="Gets all errors for the day.")
    @commands.check(utils.check_admin)
    async def error_report(self, ctx: commands.Context):
        """error_report
        ---

        Gets all the errors for the same day.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        date = datetime.utcnow().strftime("%Y-%m-%d")
        errors = await utils.select("errors",
                                    "id, message, command, error",
                                    "date_trunc('day', time)",
                                    date)
        if not errors:
            await ctx.send("No errors for {}".format(date))
        else:
            msg = "Errors:\n"
            for error in errors:
                msg += "> - {}\n".format(error)
            if len(msg) >= 2000:
                list_of_msgs = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
                for x in list_of_msgs:
                    await ctx.send(x)
            else:
                await ctx.send(msg)

    @commands.command(name="get-reports", help="Gets all the reports for the current day")
    @commands.check(utils.check_admin)
    async def get_reports(self, ctx: commands.Context):
        """get-reports
        ---

        Gets all the reports for the current day

        Arguments:
        ---
            ctx {Discord.ext.commands.Context} -- Context of the command.
        """
        date = datetime.utcnow().strftime("%Y-%m-%d")
        reports = await utils.select("reports",
                                     "name, message",
                                     "date_trunc('day', time)",
                                     date)
        if not reports:
            await ctx.send("No reports for {}".format(date))
        else:
            msg = "Reports:\n"
            for report in reports:
                msg += "> - {}\n".format(report)
            if len(msg) >= 2000:
                list_of_msgs = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
                for x in list_of_msgs:
                    await ctx.send(x)
            else:
                await ctx.send(msg)

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
        channels = self.bot.get_channel(await utils.select("admin_channels", "id", "log", "t")[0])
        for channel in channels:
            to_send = self.bot.get_channel(channel)
            await to_send.send("Role: {} was deleted".format(role.name))
