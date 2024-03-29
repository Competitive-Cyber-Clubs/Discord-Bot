"""Cog for tasks that are scheduled to run"""
from datetime import datetime
from discord.ext import commands, tasks
from bot import utils


class TaskCog(commands.Cog, name="Tasks"):
    """
    Task Cog

        Cog that holds tasks for the bot

    **Tasks:**
        - :ref:`error_report`: Output all errors for a day to admin channels.

    """

    def __init__(self, bot):
        self.bot = bot
        if self.bot.daily_reporting:
            self.report_errors.start()  # pylint: disable=no-member

    @commands.command(name="disable-daily-reporting")
    @commands.check(utils.check_admin)
    async def disable_error_reporting(self, ctx: commands.Context):
        """Disable Error Reporting for server"""
        await utils.insert("keys", ["daily-report", False])
        self.report_errors.stop()
        self.bot.daily_reporting = False
        await ctx.send("Daily reporting has been disabled")

    @commands.command(name="enable-daily-reporting")
    @commands.check(utils.check_admin)
    async def enable_error_reporting(self, ctx: commands.Context):
        """Enable Error Reporting for server"""
        await utils.insert("keys", ["daily-report", True])
        self.report_errors.start()
        self.bot.daily_reporting = True
        await ctx.send("Daily reporting has been enabled")

    @tasks.loop(hours=24.0)
    async def report_errors(self) -> None:
        """
        Report error

        Every 24 hours, all errors for the current day are sent to the admin channels.

        :return: None
        """
        date = datetime.utcnow().strftime("%Y-%m-%d")
        error_record = [
            error
            for error in await utils.select(
                "errors", "id, message, error, ack", "date_trunc('day', time)", date
            )
            if error[-1] is False
        ]
        if not error_record:
            errors = f"No errors found for {date}"
        else:
            errors = f"Errors for {date}.\n"
            for error in error_record:
                errors += f"- {error[0]}: {error[1]}; {error[2]}\n\n"
        await utils.admin_log(self.bot, errors, True)


async def setup(bot: commands.Bot) -> None:
    """Needed for extension loading"""
    await bot.add_cog(TaskCog(bot))
