"""Deals with long message sending"""
import logging
from .datahandler import select

log = logging.getLogger("bot")


async def list_message(ctx, message: list, title: str = None,):
    """list_message
    ---
    Asynchronous Function

    Breaks up messages that contain a list and sends the parts of them. Shared function between
    multiple commands.

    Arguments:
    ---
        ctx {discord.ext.commands.Context} -- Context of the command.
        message {list} -- list of items to send

    Keyword Arguments:
        title {str} -- First line of the message to send (default: {None})
    """
    msg = "{}\n".format(title.capitalize())
    for item in message:
        msg += "> - {}\n".format(item)
    if len(msg) >= 2000:
        list_of_msgs = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
        for x in list_of_msgs:
            await ctx.send(x)
        return
    await ctx.send(msg)


async def admin_log(bot, message: str, log_status: bool = True):
    """admin_log
    ---
    Asynchronous Function

    Log the :refs:`message` to the admin channels.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
        log_status {[type]} -- [description]
    """
    channels = await select("admin_channels", "id", "log", log_status)
    for channel in channels:
        to_send = bot.get_channel(channel)
        if to_send is None:
            log.warning('No channel found for id {}'.format(channel))
        elif len(message) > 2000:
            log.warning("Log message length too long. Will not be send")
        else:
            await to_send.send(message)
