"""
Imports utility features
datahandler deals with the database management.
    - utils.create makes default tables.
    - utils.fetch fetches a query from the table selected.
    - utils.insert adds a row the databases.
    - utils.update updates a row.
    - utils.delete deletes a row.
logger makes the logger
    - utils.make_loggers creates logger that outputs to a file and stream.
shared has various checks that are used by cogs.
    - utils.check_admin checks to see if the user id is in the bot_admin table.
    - utils.check_react checks to see if the correct reaction was added by the correct user.
    - utils.FailedCheck is a expection that is made if the check fails.
validate is a csv parser
    - utils.school_check checks if the input is a valid school name.
    - utils.state_list returns all schools in a state.
"""
from .datahandler import create, fetch, insert, update, delete
from .logger import make_logger
from .shared import check_admin, check_react, FailedCheck
from .validate import school_check, state_list
__all__ = ["create", "fetch", "insert", "update", "delete",
           "make_logger",
           "check_admin", "check_react", "FailedCheck",
           "school_check", "state_list"]
