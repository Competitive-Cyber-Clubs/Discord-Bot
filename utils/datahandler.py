"""Handles all Postgresql data and tables"""
import os
import logging
import asyncio
from datetime import datetime
import psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger("bot")
DATABASE_URL = os.getenv('DATABASE_URL')

connection = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor = connection.cursor()


def create():
    "Creates tables if they do not exist at startup"
    commands = ["""
CREATE TABLE IF NOT EXISTS schools(
school text NOT NULL DEFAULT '',
region text NOT NULL DEFAULT '',
color text NOT NULL DEFAULT ' ',
id bigint NOT NULL DEFAULT '0',
added_by text NOT NULL DEFAULT '',
added_by_id bigint NOT NULL DEFAULT '0',
PRIMARY KEY (school)
);""", """
CREATE TABLE IF NOT EXISTS bot_admins(
id bigint UNIQUE NOT NULL DEFAULT '0',
name text NOT NULL DEFAULT '',
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS admin_channels(
name text NOT NULL DEFAULT '',
id bigint NOT NULL DEFAULT '0',
log bool DEFAULT False,
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS regions(
name text NOT NULL DEFAULT '',
id bigint NOT NULL DEFAULT '0',
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS errors(
id int NOT NULL DEFAULT '0',
error text NOT NULL DEFAULT '',
time text NOT NULL,
PRIMARY KEY (id)
);""", """
CREATE TABLE IF NOT EXISTS keys(
key text NOT NULL DEFAULT '',
value text NOT NULL DEFAULT '',
PRIMARY KEY (key)
);""", """
CREATE TABLE IF NOT EXISTS messages(
name text NOT NULL DEFAULT '',
message text NOT NULL DEFAULT '',
PRIMARY KEY (name)
);"""]
    for i in commands:
        cursor.execute(i)


def format_step(table: str):
    """Sets ups the formatstring to be used in insert"""
    if table == "schools":
        query_str = "INSERT INTO schools \
                     (school, region, color, id, added_by, added_by_id) \
                      VALUES (%s, %s, %s, %s, %s, %s);"
    elif table == "admin_channels":
        query_str = "INSERT INTO admin_channels (name, id, log)\
                      VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;"
    elif table == "bot_admins":
        query_str = "INSERT INTO bot_admins \
                    (name, id) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
    elif table == "regions":
        query_str = "INSERT INTO regions \
                     (name, id) VALUES (%s, %s);"
    elif table == "errors":
        query_str = "INSERT INTO errors\
                      (id, error, time) \
                       VALUES (%s, %s, %s)"
    else:
        log.error("Table not found.")
        return "error"
    return query_str


@asyncio.coroutine
def insert(table: str, data: list):
    "Adds data to existing tables"
    format_str = format_step(table)
    try:
        if table == "schools":
            cursor.execute(format_str,
                           (data[0], data[1],
                            data[2], data[3],
                            data[4], data[5]))
        elif table in ["bot_admins", "regions"]:
            cursor.execute(format_str,
                           (data[0], data[1]))
        elif table in ["errors", "admin_channels"]:
            data.append(datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"))
            cursor.execute(format_str,
                           (data[0], data[1], data[2]))
        connection.commit()
        return None
    except psycopg2.Error as pge:
        log.error(pge)
        cursor.execute("ROLLBACK")
        return "error"


@asyncio.coroutine
async def fetch(table: str, ident: str):
    """Retrives ident from the table of choice."""
    try:
        format_str = "SELECT %s FROM %s;"
        cursor.execute(format_str, (AsIs(ident),
                                    AsIs(table)))
        fetched = cursor.fetchall()
    except psycopg2.Error as pge:
        log.error(pge)
    if ident == "*" or ident.find(",") != -1:
        result = fetched
    else:
        result = []
        for _, x in enumerate(fetched):
            result.append(x[0])
    return result


@asyncio.coroutine
async def select(table: str, ident: str, where: str, where_value: str):
    """Selects one row from the table based on selector"""
    try:
        format_str = "SELECT %s FROM %s WHERE %s = %s"
        cursor.execute(format_str, (
            AsIs(ident),
            AsIs(table),
            AsIs(where),
            where_value
        ))
        fetched = cursor.fetchone()[0]
        return fetched
    except psycopg2.Error as pge:
        log.error(pge)
        cursor.execute("ROLLBACK")


@asyncio.coroutine
async def update(table: str, ident: str, where: str, new_value: str):
    """Updates a value in the table"""
    try:
        format_str = "UPDATE %s SET %s = %s where %s = %s"
        cursor.execute(format_str, (
            AsIs(table),
            AsIs(ident),
            new_value,
            AsIs(ident),
            where
        ))
        connection.commit()
    except psycopg2.Error as pge:
        log.error(pge)
        cursor.execute("ROLLBACK")


@asyncio.coroutine
async def delete(table: str, indent: str, value: str):
    """Removes an entry from the table"""
    try:
        format_str = "DELETE FROM %s WHERE %s = %s"
        cursor.execute(format_str, (
            AsIs(table),
            AsIs(indent),
            value
        ))
        connection.commit()
    except psycopg2.Error as pge:
        log.error(pge)
        cursor.execute("ROLLBACK")
