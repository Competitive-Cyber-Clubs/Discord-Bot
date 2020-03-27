"""Imports utility features
It deals with the database management.
    - utils.create makes default tables.
    - utils.fetch fetches a query from the table selected.
    - utils.insert adds a row the databases.
    - utils.update updates a row.
    - utils.delete deletes a row.
"""
from .datahandler import create, fetch, insert, update, delete
from .logger import make_logger
from .shared import check_admin, check_react, FailedCheck
__all__ = ["create", "fetch", "insert", "update", "delete",
           "make_logger", "check_admin", "check_react", "FailedCheck"]
