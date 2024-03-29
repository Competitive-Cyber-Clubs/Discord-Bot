"""Cog the preforms health functions"""
from datetime import datetime
from discord.ext import commands
import discord
from bot import utils
import cyberjake


async def managed_role_check(role: discord.Role) -> [bool, str]:
    """Managed role check

    Checks to see if the updated one was one that the bot cares about.

    :param role: the role was cared about or does not return.
    :type role: str
    :return: If role was found and table the role is in
    """
    for table in ["schools", "regions"]:
        if await utils.select(table, "id", "id", role.id):
            return True, table
    return False, "error"


class HealthCog(commands.Cog, name="Health"):
    """
    HealthCog


    Cog that holds the health commands and is responsible for updating the
    tables when roles change in discord.

    **Commands:**
        - `check-health`: Makes sure that all the roles in the tables `schools` and `regions` map
            to roles in the discord server.

    **Events:**
        - `on_guild_role_update`: Event that is triggered when a role is updated.

        - `on_guild_role_delete`: Event that is triggered when a role is deleted.

    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        """
        Cog check

        Makes all the commands in health admin only

        :param ctx: Command context
        :return: User in bot_admins table
        :rtype: bool
        """
        return await utils.check_admin(ctx)

    @commands.command(name="check-health", help="Checks health of roles for schools and regions")
    async def check_health(self, ctx: commands.Context) -> None:
        """Check health

        Checks health of roles for schools and regions. It pulls all the IDs for school and
        region roles. Then compares the names of the matching ids to see if they match. If
        they match then added to a list called success and if the check fails then then
        both names are added to a list called fail.


        :param ctx: Command context
        :return:
        """
        async with ctx.typing():
            table_schools = await utils.fetch("schools", "school")
            regions = await utils.fetch("regions", "name")
            success, fail = [], []
            for roles in [table_schools, regions]:
                for role in roles:
                    try:
                        role_name = discord.utils.get(ctx.guild.roles, name=role)
                        if role_name.name == role:
                            success.append(role_name)
                        else:
                            fail.append((role_name, role))
                    except AttributeError:
                        self.bot.log.error(f"Attribute error with role {role}")
                        fail.append((role, None))

        message = f"There were {len(success)} successes and {len(fail)} failures"
        await cyberjake.make_embed(ctx, "28b463", title="Check Complete", description=message)

    @commands.command(
        name="get-status",
        help="Gets all errors or reports for the day.",
        description="Admin Only Feature",
    )
    async def get_status(self, ctx: commands.Context, which: str, ack: bool = False):
        """Get Status

        Get user reports or errors for the current day

        :param ctx: Command Context
        :param which: Either reports or errors
        :type which: str
        :param ack: Get acknowledged errors
        :type ack: bool
        :return: None
        """
        if which == "errors":
            columns = "id, message, command, error, ack"
        elif which == "reports":
            columns = "name, message"
        else:
            return await cyberjake.error_message(ctx, "Please pick a valid option.")
        date = datetime.utcnow().strftime("%Y-%m-%d")
        results = await utils.select(which, columns, "date_trunc('day', time)", date)
        if not results:
            await cyberjake.make_embed(
                ctx, "28b463", title="Success", description=f"No {which} for {date}"
            )
        else:
            results_string = []
            for result in results:
                if result[-1] == ack and which == "errors":
                    results_string.append(" ".join(map(str, result)))
            await cyberjake.list_message(ctx, results_string, which)

    @commands.command(
        name="test-log",
        help="Tests to make sure that that logging feature works.",
        description="Admin Only Feature",
    )
    async def check_log(self, ctx: commands.Context):
        """Test log

        Sends a debugging log

        :param ctx: Command context
        :return: None
        """
        await utils.admin_log(self.bot, "TESTING LOG: True", True)
        await utils.admin_log(self.bot, "TESTING LOG: False", False)
        await cyberjake.make_embed(ctx, color="28b463", title="Test Complete")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role) -> None:
        """Role update

        Triggered when a role is edited. Logs the old name and new name then updates the name in the
        table.

        :param before: Discord role before it was edited.
        :type before: discord.Role
        :param after: Discord role after it was edited.
        :type after: discord.Role
        :return: None
        """
        managed, _ = await managed_role_check(before)
        self.bot.log.debug(f"Role: {before.name} Managed: {managed}")
        if managed:
            await utils.update("schools", "school", before.name, after.name)
            self.bot.log.warning(f'Role "{before.name}" was updated. It is now {after.name}')
            await utils.admin_log(self.bot, f"Old role {before} now new role {after}")
        else:
            self.bot.log.info(f"Old role {before} now new role {after}")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        """Role delete

        Triggered when a role is deleted. Will only delete an entry if it existed in the schools or
        regions table.

        :param role: Role that was deleted.
        :type role: discord.Role
        :return: None
        """
        managed, table = await managed_role_check(role)
        if managed:
            await utils.delete("schools", "id", role.id)
            self.bot.log.warning(f'Role "{role.name}" was deleted. It was in {table}')
        else:
            self.bot.log.info(f'Role "{role.name}" was deleted. It was not a managed role')

        await utils.admin_log(self.bot, f"Role: {role.name} was deleted", True)


async def setup(bot: commands.Bot) -> None:
    """Needed for extension loading"""
    await bot.add_cog(HealthCog(bot))
