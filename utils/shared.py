"""Shared functions between cogs and main program"""
from .datahandler import fetch


class FailedCheck(Exception):
    """Exception if react checks fail"""


def check_admin(ctx):
    """Checks to see if message author is in bot_admins"""
    returned = [int(id) for id in fetch("bot_admins", "id")]
    return ctx.message.author.id in returned


def check_react(ctx, user, reaction, expected_react):
    """Checks to see if the reaction is the one needed"""
    return user == ctx.author and str(reaction.emoji) == expected_react
