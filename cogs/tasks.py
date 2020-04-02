"""Cog for tasks that are scheduled to run"""
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
        self.error_report.start()  # pylint: disable=no-member

    @tasks.loop(hours=24.0)
    async def error_report(self):
        """error_report
        ---
        Every 24 hours, all error for the current day are send to the admin channels.
        """
        date = datetime.utcnow().strftime("%Y-%m-%d")
        errors = await utils.select("errors", "*", "date_trunc('day', time)", date)
        channels = await utils.select("admin_channels", "id", "log", "t")
        for channel in channels:
            each_channel = self.bot.get_channel(channel)
            for error in errors:
                await each_channel.send(error)
