"""utility features and functions
---

datahandler
---
Deals with the database management:
    `utils.create` makes default tables.
    `utils.fetch` fetches a query from the table selected.
    `utils.select` fetches one row based on the selector values
    `utils.insert` adds a row the databases.
    `utils.update` updates a row.
    `utils.delete` deletes a row.

logger
---
makes the logger:
    `utils.make_logger` creates logger that outputs to a file and stream.

shared:
---
Various checks that are used by cogs:

    `utils.check_admin` checks to see if the user id is in the bot_admin table.
    `utils.check_react` checks to see if the correct reaction was added by the correct user.
    `utils.FailedReactionCheck` is a exception that is made if the check fails.

validate
---
Deals with school_list.csv:

    `utils.school_check` checks if the input is a valid school name.
    `utils.state_list` returns all schools in a state.
    `utils.school_search` returns a list of possible schools
    `utils.region_select` returns the region that a school is in.

messages
---
Deals with various messaging cases:

    `utils.list_messages take a list and sends it as a message
    `utils.admin_log` logs anything to the admin_channels
    `utils.make_embed` returns an initial discord.Embed
    `utils.TF_emoji` returns str for TRUE/FALSE emoji
"""
from .datahandler import table_create, fetch, select, insert, update, delete
from .logger import make_logger
from .shared import check_admin, check_react, FailedReactionCheck, TF_emoji
from .validate import (
    school_check,
    state_list,
    school_search,
    region_select,
    update_list,
)
from .messages import list_message, admin_log, make_embed

__all__ = [
    "table_create",
    "fetch",
    "select",
    "insert",
    "update",
    "delete",
    "make_logger",
    "check_admin",
    "check_react",
    "FailedReactionCheck",
    "TF_emoji",
    "school_check",
    "state_list",
    "school_search",
    "region_select",
    "update_list",
    "list_message",
    "admin_log",
    "make_embed",
]
