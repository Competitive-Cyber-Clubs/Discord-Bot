"""Cog for tasks that are scheduled to run"""
import logging
from datetime import datetime
from discord.ext import commands, tasks
import utils


class TaskCog(commands.Cog, name="Tasks"):
    """TaskCog
    ---

    Cog that holds tasks for the bot

    Tasks
    ---
        :ref:`error_report`: Output all errors for a day to admin channels.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("bot")
        self.report_errors.start()  # pylint: disable=no-member

    @tasks.loop(hours=24.0)
    async def report_errors(self):
        """report_errors
        ---
        Every 24 hours, all errors for the current day are send to the admin channels.
        """
        date = datetime.utcnow().strftime("%Y-%m-%d")
        error_record = await utils.select("errors", "message, error",
                                          "date_trunc('day', time)", date)
        if not error_record:
            errors = "No errors found for {}".format(date)
        else:
            errors = "Errors for {}.\n".format(date)
            for error in error_record:
                errors += "- {}; {}\n".format(*error)
        await utils.admin_log(self.bot, errors, True)
