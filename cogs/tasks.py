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
        `bot` `discord.commands.Bot` -- The bot class that deals with all the commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("bot")
        self.report_errors.start()  # pylint: disable=no-member

    @tasks.loop(hours=24.0)
    async def report_errors(self):
        """error_report
        ---
        Every 24 hours, all error for the current day are send to the admin channels.
        """
        date = datetime.utcnow().strftime("%Y-%m-%d")
        errors = await utils.select("errors", "*", "date_trunc('day', time)", date)
        if not errors:
            errors = "No errors found for {}".format(date)
        else:
            channels = await utils.select("admin_channels", "id", "log", "t")
            for channel in channels:
                to_send = self.bot.get_channel(channel)
                if to_send is None:
                    self.log.warning('No channel found for id {}'.format(channel))
                for error in errors:
                    await to_send.send(error)
