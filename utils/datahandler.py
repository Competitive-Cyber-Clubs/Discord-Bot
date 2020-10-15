"""Handles all postgresql data and tables"""
import os
import psycopg2
from psycopg2.extensions import AsIs
from .tables import tables
from .logger import make_logger

# Imports the main logger
log = make_logger("database", os.getenv("LOG_LEVEL"))

# Creates the connection to the database
connection = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
cursor = connection.cursor()


def table_create() -> None:
    """table_create

    Creates tables if they do not exist at startup. All tables are pulled from tables.py

    """
    for table in tables:
        cursor.execute(table)


def format_step(table: str) -> str:
    """format_step
    ---

    Returns the format string to be used in insert. This was split from insert to make it less
        complex and easier to read.

    Arguments:
    ---
        table {str} -- The name of the table for the insert

    Returns:
    ---
        str -- Returns a string that will be used for cursor execution
    """
    if table == "schools":
        query_str = (
            "INSERT INTO schools"
            "(school, region, color, id, added_by, added_by_id) "
            "VALUES (%s, %s, %s, %s, %s, %s);"
        )
    elif table == "errors":
        query_str = (
            "INSERT INTO errors"
            "(id, command, message, error, time) "
            "VALUES (%s, %s, %s, %s, %s);"
        )
    elif table == "reports":
        query_str = (
            "INSERT INTO reports"
            "(id, name, name_id, message, time) "
            "VALUES (%s, %s, %s, %s, %s);"
        )
    elif table == "admin_channels":
        query_str = (
            "INSERT INTO admin_channels (name, id, log) "
            "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;"
        )
    elif table == "bot_admins":
        query_str = "INSERT INTO bot_admins (name, id) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
    elif table == "regions":
        query_str = "INSERT INTO regions (name, id) VALUES (%s, %s)"
    else:
        log.error("Table not found.")
        return "error"
    return query_str


def result_parser(column: str, fetched: list) -> list:
    """result_parser
    ---

    Arguments:
    ---
        column {str} -- The name of the column(s) only used to determine how to parse the results.
        fetched {list} -- The results pulled from the table.

    Returns:
    ---
        list -- A normal list or a list of tuples.
    """
    # fetched is a list so it does not need breaking up
    if column == "*" or column.find(",") != -1:
        result = fetched
    # Breaks up the tuples to a standard list.
    else:
        result = []
        for _, x in enumerate(fetched):
            result.append(x[0])
    return result


async def insert(table: str, data: list) -> [None, str]:
    """insert
    ---

    Asynchronous Function

    Inserts a new row to an existing table. Get the string to execute with from :ref:`format_step`.

    Arguments:
    ---
        table {str} -- c to perform the insert on
        data {list} -- The data that gets placed into the format_str

    Returns:
    ---
        str -- In the event of an error inserting into the table the string 'error' will be
            returned. If there is no error then 'None' will be returned.
    PostgreSQL Equivalent:
    ---
    INSERT into :ref:`table` VALUE (:ref:`*data`);
    """
    format_str = format_step(table)
    if format_str == "error":
        return "error"
    log.debug(format_str, *data)
    try:
        # Tables with 6 values
        if table == "schools":
            cursor.execute(format_str, (data[0], data[1], data[2], data[3], data[4], data[5]))
        # Tables with 5 values
        elif table in ["errors", "reports"]:
            cursor.execute(format_str, (data[0], data[1], data[2], data[3], data[4]))
        # Tables with 3 values
        elif table == "admin_channels":
            cursor.execute(format_str, (data[0], data[1], data[2]))
        # Tables with 2 values
        elif table in ["bot_admins", "regions"]:
            cursor.execute(format_str, (data[0], data[1]))
        connection.commit()
        return None
    except psycopg2.Error as pge:
        log.error(pge)
        cursor.execute("ROLLBACK")
        return "error"


async def fetch(table: str, column: str) -> list:
    """fetch
    ---

    Asynchronous Function

    Retrieves values from the :ref:`column` from the :ref:`table`.

    Arguments:
    ---
        table {str} -- Name of the table that data is being fetched from.
        column {str} -- The column(s) that is being fetched. Multiple columns need to comma
            separated, if all columns are wanted then use '*'.

    Returns:
    ---
        list -- A list of tuples for '*' or multiple columns. For one column it is a list.

    Postgresql Equivalent:
    ---
    SELECT :ref:`column` from :ref:`table`;
    """
    try:
        format_str = "SELECT %s FROM %s;"
        cursor.execute(format_str, (AsIs(column), AsIs(table)))
        fetched = cursor.fetchall()
        return result_parser(column, fetched)
    except psycopg2.Error as pge:
        log.error(pge)


async def select(
    table: str, column: str, where_column: str, where_value: str, symbol: (str, bool) = "="
) -> list:
    """select
    ---

    Asynchronous Function

    Selects one row from the table based on selector.


    Arguments:
    ---
        table {str} -- Name of the table that data is being fetched from.
        column {str} -- The column(s) that is being fetched. Multiple columns need to comma
            separated, if all columns are wanted then use '*'.
        where_column {str} -- The column that is going have the value of :ref:`where_value`.
        where_value {str} -- The value that you are matching.
        symbol {str} -- [description] (default: {"="})

    Returns:
    ---
        list -- List of values that are the results.

    Postgresql Equivalent:
    ---
    SELECT :ref:`column` FROM :ref:`table` WHERE :ref:`where_column` :ref:`symbol` :ref:`where_value`;  # noqa: E501 pylint: disable=line-too-long
    """
    try:
        format_str = "SELECT %s FROM %s WHERE %s %s %s;"
        cursor.execute(
            format_str,
            (AsIs(column), AsIs(table), AsIs(where_column), AsIs(symbol), where_value),
        )
        fetched = cursor.fetchall()
        return result_parser(column, fetched)
    except psycopg2.Error as pge:
        log.error(pge)
        cursor.execute("ROLLBACK")


async def update(table: str, column: str, where_value: str, new_value: str) -> None:
    """Update
    ---

    Asynchronous Function

    Updates a value in the table

    Arguments:
        table {str} -- Name of the table that the data is being updated on.
        column {str} -- The column that is being updated. Multiple columns are not supported.
        where_value {str} -- The value that is going to be updated.
        new_value {str} -- The new value for :ref:`where_value`

    Postgresql Equivalent:
    ---
    UPDATE :ref:`table` SET :ref:`column` = :ref:`new_value` WHERE :ref:`column` = :ref:`where_value`; # noqa: E501 pylint: disable=line-too-long
    """
    try:
        format_str = "UPDATE %s SET %s = %s where %s = %s"
        cursor.execute(
            format_str,
            (AsIs(table), AsIs(column), new_value, AsIs(column), where_value),
        )
        connection.commit()
    except psycopg2.Error as pge:
        log.error(pge)
        cursor.execute("ROLLBACK")


async def delete(table: str, column: str, value: str) -> None:
    """Delete
    ---
    Asynchronous Function

    Removes an entry from the table where :ref:`value` is equal.

    Arguments:
    ---
        table {str} -- Name of the table that the data is being deleted from.

        column {str} -- The column to which the :ref:`value` is going to match.

        value {str} -- The value in the row which is going to match to a value in :ref:`column`

    Postgresql Equivalent:
    ---
    DELETE FROM :ref:`table` WHERE :ref:`column` = :ref:`value`;
    """
    try:
        format_str = "DELETE FROM %s WHERE %s = %s"
        cursor.execute(format_str, (AsIs(table), AsIs(column), value))
        connection.commit()
    except psycopg2.Error as pge:
        log.error(pge)
        cursor.execute("ROLLBACK")
