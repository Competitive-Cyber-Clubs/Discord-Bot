"""Shared functions between cogs and main program"""
from .datahandler import fetch


def check_admin(ctx):
    """Checks to see if message author is in bot_admins"""
    returned = [int(id) for id in fetch("bot_admins", "id")]
    return ctx.message.author.id in returned
