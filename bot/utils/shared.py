"""Shared functions between cogs and main program"""
import discord

from .datahandler import fetch


class FailedReactionCheck(Exception):
    """FailedReactionCheck
    ---
    Exception if react checks fail
    """


async def check_admin(ctx) -> bool:
    """Check Admin

    Checks to see if message author is in bot_admins table

    :param ctx:
    :type ctx: discord.ext.commands.Context
    :return: Message author is in bot_admins.
    :rtype: bool
    """
    return ctx.message.author.id in [int(user_id) for user_id in await fetch("bot_admins", "id")]


async def TF_emoji(status: bool) -> str:
    """True or False emoji

    :param status: Return the true value emoji
    :type status: bool
    :return: Check mark or X
    :rtype str:
    """
    return ":white_check_mark:" if status else ":x:"


async def check_react(
    ctx, member: discord.Member, reaction: discord.Reaction, expected_react: str
) -> bool:
    """Check reaction

    Checks if the reaction on a message is correct and send by the same member that it was needed
        from.

    :param ctx: Message context
    :param member: Member who reacted to the message
    :type member: discord.Member
    :param reaction: Reaction that was added to the message
    :type reaction: discord.Reaction
    :param expected_react: String of wanted reaction
    :type expected_react: str
    :return: Correct reaction from the correct member.
    :rtype bool:
    """
    return member == ctx.author and str(reaction.emoji) == expected_react
