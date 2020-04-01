"""Shared functions between cogs and main program"""
from .datahandler import fetch


class FailedReactionCheck(Exception):
    """FailedReactionCheck
    ---
    Exception if react checks fail
    """


async def check_admin(ctx):
    """check_admin
    ---
    Checks to see if message author is in bot_admins

    Arguments:
    ---
        ctx {discord.ext.commands.Context} -- Context of which the check was called.

    Returns:
    ---
        bool -- Returns 'TRUE' if the message author is in bot_admins.
    """
    returned = [int(id) for id in await fetch("bot_admins", "id")]
    return ctx.message.author.id in returned


async def check_react(ctx, user, reaction, expected_react):
    """check_reach
    ---
    Checks if the reaction on a message is correct and send by the same user that it was needed
        from.

    Arguments:
    ---
        ctx {discord.ext.commands.Context} -- Context of which the check was called.
        user {discord.User} -- User the reacted to the message
        reaction {discord.Reaction} -- The reaction that was added to the message
        expected_react {str} -- The desired reaction.

    Returns:
    ---
        bool -- Return 'TRUE' if it was the correct reaction from the correct user.
    """
    return user == ctx.author and str(reaction.emoji) == expected_react
