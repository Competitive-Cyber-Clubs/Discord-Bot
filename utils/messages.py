"""Deals with long message sending"""
import logging
import random
import discord
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
    msg = ""
    part = 0
    for item in message:
        msg += "- {}\n".format(item)
    if len(msg) >= 2000:
        part += 1
        list_of_msgs = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
        for x in list_of_msgs:
            part_embed = await make_embed(ctx, title=title.capitalize(),
                                          description=x)
            await ctx.send(embed=part_embed)
    else:
        embed = await make_embed(ctx, title=title.capitalize(),
                                 description=msg)
        await ctx.send(embed=embed)


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
    if len(message) > 2000:
        log.warning("Log message length too long, it will not be sent. Length: {}".format(
            len(message)))
    else:
        channels = await select("admin_channels", "id", "log", log_status)
        for channel in channels:
            to_send = bot.get_channel(channel)
            if to_send is None:
                log.warning('No channel found for id {}'.format(channel))
            else:
                embed = discord.Embed(title="Errors:", description=message,
                                      color=discord.Color(int("FF0000", 16)))
                await to_send.send(embed=embed)


async def make_embed(ctx, color: str = None, **kwargs):
    """make_embed
    ---

    Asynchronous Function

    Makes and sends a discord embed

    Arguments:
    ---
        ctx {discord.ext.commands.Context} -- Context of the command.
    """
    if not color:
        kwargs["color"] = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)  # nosec
    elif isinstance(color, str):
        kwargs["color"] = discord.Color(int(color, 16))
    embed = discord.Embed(timestamp=ctx.message.created_at,
                          **kwargs)
    return embed
