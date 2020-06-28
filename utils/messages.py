"""Deals with long message sending"""
import logging
import random
import discord
from .datahandler import select

log = logging.getLogger("bot")


async def list_message(ctx, message: list, title: str, **kwargs: dict):
    """list_message
    ---
    Asynchronous Function

    Breaks up messages that contain a list and sends the parts of them. Shared function between
    multiple commands.


    I'm sorry for everyone dealing with this function. It is not clean and I have commented to
    the best that I can.

    Arguments:
    ---
        ctx {discord.ext.commands.Context} -- Context of the command.
        message {list} -- list of items to send.
        title {str} -- First line of the message to send.
    """
    joined_message = len("".join(message))
    list_of_embeds = []
    part = 1
    item = 0
    amount_of_embeds = len(range(0, joined_message, 1500))
    for _ in range(amount_of_embeds):
        # Each embed can only be 6000 characters so if the length is over that more are created
        embed = await make_embed(ctx, title=title, send=False, **kwargs)
        for _ in range(2):
            temp_msg = ""
            while len(temp_msg) < 1024:
                # Each field can only be 1024 characters
                try:
                    if len(temp_msg + "- {}\n".format(message[item])) > 1024:
                        # If the new item is going to make it over the 1024 limit then skip it.
                        break
                    temp_msg += "- {}\n".format(message[item])
                    item += 1
                except IndexError:
                    # Error happens when there the length of temp_msg is still under 1000 but
                    # no items left.
                    break
            if len(temp_msg) > 0:
                # Blank messages can occur and this filters them out
                embed.add_field(name="Part: {}".format(part), value=temp_msg, inline=True)
                part += 1
        list_of_embeds.append(embed)

    for item in list_of_embeds:
        if len(item.fields) > 0:
            await ctx.send(embed=item)
        else:
            log.warning("Empty embed")


async def admin_log(bot, message: str, log_status: bool = True):
    """admin_log
    ---
    Asynchronous Function

    Log the :refs:`message` to the admin channels.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
        log_status {boot} -- If the log will be sent to logging channels or non logging channels
    """
    if len(message) > 2000:
        message = "Log message length too long, it will not be sent. Length: {}".format(
            len(message)
        )
        log.warning(message)

    channels = await select("admin_channels", "id", "log", log_status)
    for channel in channels:
        to_send = bot.get_channel(channel)
        if to_send is None:
            log.warning("No channel found for id {}".format(channel))
        else:
            embed = discord.Embed(
                title="Log Update:", description=message, color=discord.Color(int("FF0000", 16)),
            )
            await to_send.send(embed=embed)


async def make_embed(ctx, color: [str, int] = None, send: bool = True, **kwargs) -> discord.Embed():
    """make_embed
    ---

    Asynchronous Function

    Makes and sends a discord embed

    Arguments:
    ---
        ctx {discord.ext.commands.Context} -- Context of the command.
        color {str} -- Hex code for color. If empty random one will be added (default: {None})
        send {bool} -- If make_embed sends the embed. Only false is the function adds items to the
                        embed such as fields.
    """
    if not color:
        kwargs["color"] = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)  # nosec
    elif isinstance(color, str):
        kwargs["color"] = discord.Color(int(color, 16))

    embed = discord.Embed(timestamp=ctx.message.created_at, **kwargs)

    if "footer" in kwargs:
        embed.set_footer(text=kwargs["footer"])
    if send:
        await ctx.send(embed=embed)
    else:
        return embed
