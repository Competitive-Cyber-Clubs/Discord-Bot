"""Handles all postgresql data and tables"""
import os
import typing

import psycopg2.errors
from psycopg2 import pool
from psycopg2.extensions import AsIs
from .tables import tables
from .logger import make_logger

# Imports the database logger
log = make_logger("database", os.getenv("LOG_LEVEL", "INFO"))

# Creates the connection to the database

db_pool = pool.ThreadedConnectionPool(minconn=1, maxconn=15, dsn=os.getenv("DATABASE_URL").strip())
DuplicateError = psycopg2.errors.lookup("23505")


def table_create() -> None:
    """Table_create

    Create tables if they do not exist at startup. All tables are pulled from tables.py
    :return:
    """
    with db_pool.getconn() as con:
        with con.cursor() as pg_cursor:
            try:
                for table in tables:
                    pg_cursor.execute(table)
                con.commit()
            except psycopg2.Error as pge:
                log.error(pge)
                con.rollback()


def _format_step(table: str) -> str:
    """
    Returns the format string to be used in insert. This was split from insert to make it less
    complex and easier to read.

    :param table: Name of the table that is being used
    :type table: str
    :return: String that will be used for cursor execution
    :rtype: str
    """
    match table:
        case "schools":
            query_str = (
                "INSERT INTO schools"
                "(school, region, color, id, added_by, added_by_id) "
                "VALUES (%s, %s, %s, %s, %s, %s);"
            )
        case "errors":
            query_str = (
                "INSERT INTO errors"
                "(id, command, message, error, time, ack) "
                "VALUES (%s, %s, %s, %s, %s, %s);"
            )
        case "reports":
            query_str = (
                "INSERT INTO reports"
                "(id, name, name_id, message, time) "
                "VALUES (%s, %s, %s, %s, %s);"
            )
        case "admin_channels":
            query_str = (
                "INSERT INTO admin_channels (name, id, log) "
                "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;"
            )
        case "bot_admins":
            query_str = "INSERT INTO bot_admins (name, id) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
        case "regions":
            query_str = "INSERT INTO regions (name, id) VALUES (%s, %s);"
        case "keys":
            query_str = "INSERT INTO keys (key, value) VALUES (%s, %s);"
        case _:
            log.error(f"Table {table} not found.")
            return "error"
    return query_str


def _result_parser(column: str, fetched: list) -> typing.Union[list, typing.List[typing.Tuple]]:
    """Parse the query results

    :param column: The name of the column(s) only used to determine how to parse the
            results. Multiple commas need ','
    :type column: str
    :param fetched: Results from SQL query
    :type fetched: list
    :return: A normal list or a list of tuples.
    :rtype: list
    """
    # fetched is a list so it does not need breaking up
    if column == "*" or column.find(",") != -1:
        result = fetched
    # Breaks up the tuples to a standard list.
    else:
        result = [x[0] for x in fetched]
    return result


async def insert(table: str, data: list) -> typing.Union[None, str]:
    """Insert into a table

    **Asynchronous Function**

    Inserts a new row to an existing table. Get the string to execute with from _format_step()

    **PostgreSQL Equivalent:**

    INSERT into **table** VALUE (**data**);

    :param table: Table to perform the insert on
    :type table: str
    :param data: Data that gets placed into the format_str
    :type data: list
    :return: In the event of an error inserting into the table the string 'error' will be
            returned. If there is no error then 'None' will be returned.
    :rtype: str
    """
    format_str = _format_step(table)
    if format_str == "error":
        return "error"
    log.debug(f'String: {format_str} Data {" ".join(map(str, data))}')
    with db_pool.getconn() as con, con.cursor() as pg_cursor:
        try:
            pg_cursor.execute(format_str, data)
            con.commit()
            return None
        except psycopg2.Error as pge:
            log.error(pge)
            con.rollback()
            if isinstance(pge, DuplicateError):
                return "duplicate"
            return "error"


async def fetch(table: str, column: str) -> list:
    """Fetch a single column from a table

    **Asynchronous Function**

    Retrieves the full column values for **column** from the **table**.

    **Postgresql Equivalent:**

    SELECT **column** FROM **table**;

    :param table: Table that data is being fetched from.
    :type table: str
    :param column:
    :type column: str
    :return: List of values
    :rtype: list
    """
    with db_pool.getconn() as con, con.cursor() as pg_cursor:
        try:
            format_str = "SELECT %s FROM %s;"
            pg_cursor.execute(format_str, (AsIs(column), AsIs(table)))
            fetched = pg_cursor.fetchall()
            result = _result_parser(column, fetched)
            return result
        except psycopg2.Error as pge:
            log.error(pge)
            con.rollback()
            return []


async def select(
    table: str,
    column: str,
    where_column: str,
    where_value: typing.Union[str, bool, int],
    symbol: [str, bool] = "=",
) -> list:
    """Choice specific roles to return

    **Asynchronous Function**


    **Postgresql Equivalent:**

    SELECT :ref:`column` FROM :ref:`table`
    WHERE :ref:`where_column` :ref:`symbol` :ref:`where_value`;

    :param table: Table that data is being fetched from.
    :type table: str
    :param column: Column(s) that is being fetched. Multiple columns need to comma
            separated, if all columns are wanted then use '*'.
    :type column: str
    :param where_column: Column that is going have the value of :ref:`where_value`.
    :type where_column: str
    :param where_value: Value to match.
    :type where_value: str
    :param symbol: Symbol to use in comparison. Default is '='
    :type symbol: str
    :return: List of values that are the results
    :rtype: list
    """
    with db_pool.getconn() as con, con.cursor() as pg_cursor:
        try:
            format_str = "SELECT %s FROM %s WHERE %s %s %s;"
            pg_cursor.execute(
                format_str, (AsIs(column), AsIs(table), AsIs(where_column), symbol, where_value)
            )
            fetched = pg_cursor.fetchall()
            result = _result_parser(column, fetched)
            return result
        except psycopg2.Error as pge:
            log.error(pge)
            con.rollback()
            return []


async def update(
    table: str,
    column: str,
    where_value: str,
    new_value: typing.Union[str, bool],
    where_column: str = "",
) -> None:
    """Update

    **Asynchronous Function**

    **Postgresql Equivalent:**

    UPDATE **table** SET :ref:`column` = :ref:`new_value`
    WHERE :ref:`check_column` = :ref:`where_value`;

    :param table: Table that the data is being updated on.
    :type table: str
    :param column: Column that is being updated. Multiple columns are not supported.
    :type column: str
    :param where_value: Value that is going to be updated.
    :type where_value: str
    :param new_value: Value that is the replacement
    :type new_value: str
    :param where_column: Column to select from. Multiple columns are not supported.
    :type where_column: str
    :return: None
    """
    if not where_column:
        where_column = column

    with db_pool.getconn() as con, con.cursor() as pg_cursor:
        try:
            format_str = "UPDATE %s SET %s = %s WHERE %s = %s;"
            pg_cursor.execute(
                format_str,
                (AsIs(table), AsIs(column), new_value, AsIs(where_column), where_value),
            )
            con.commit()
        except psycopg2.Error as pge:
            log.error(pge)
            con.rollback()


async def delete(table: str, column: str, value: str) -> None:
    """Delete

    **Asynchronous Function**

    Delete value from table

    **Postgresql Equivalent:**

    DELETE FROM :ref:`table` WHERE :ref:`column` = :ref:`value`;

    :param table: Table that the data is being deleted from.
    :type table: str
    :param column: Column to which the :ref:`value` is going to match.
    :type column: str
    :param value: Value in the row which is going to match to a value in :ref:`column`
    :type value: str
    :return: None
    """
    with db_pool.getconn() as con, con.cursor() as pg_cursor:
        try:
            format_str = "DELETE FROM %s WHERE %s = %s;"
            pg_cursor.execute(format_str, (AsIs(table), AsIs(column), value))
            con.commit()
        except psycopg2.Error as pge:
            log.error(pge)
            con.rollback()
