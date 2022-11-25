"""Deals with long message sending"""
import logging

import discord
from discord.ext import commands
from .datahandler import select

log = logging.getLogger("bot")


async def admin_log(bot: commands.Bot, message: str, log_status: bool = True) -> None:
    """Admin Log

    **Asynchronous Function**


    Log **message** to the admin channels.

    :param bot: Discord bot
    :type bot: discord.ext.commands.Bot
    :param message: Message to log
    :type message: str
    :param log_status: Will be sent to logging channels (true)
        or non logging channels including debug
    :type log_status: bool

    """
    if len(message) > 2000:
        log.warning("Log message length too long, it will not be sent. Length: %s", len(message))

    channels = await select("admin_channels", "id", "log", log_status)
    for channel in channels:
        to_send = bot.get_channel(channel)
        if to_send is None:
            log.warning(f"No channel found for id {channel}")
        else:
            embed = discord.Embed(
                title="Log Update:",
                description=message,
                color=discord.Color(int("FF0000", 16)),
            )
            await to_send.send(embed=embed)
    return None
