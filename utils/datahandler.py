"""Handles all Postgresql data and tables"""
import os
from datetime import datetime
import psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv

load_dotenv()


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
id bigint NOT NULL DEFAULT '0',
name text NOT NULL DEFAULT '',
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS admin_channels(
name text NOT NULL DEFAULT '',
id bigint NOT NULL DEFAULT '0',
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS regions(
name text NOT NULL DEFAULT '',
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS errors(
id int NOT NULL DEFAULT '0',
error text NOT NULL DEFAULT '',
time text NOT NULL,
PRIMARY KEY (id)
);""", """
CREATE TABLE IF NOT EXISTS misc(
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


def insert(table: str, data: list, log):
    "Adds data to existing tables"
    if table == "schools":
        format_str = "INSERT INTO schools \
                     (school, region, color, id, added_by, added_by_id) \
                      VALUES (%s, %s, %s, %s, %s, %s);"
    elif table == "bot_admins":
        format_str = "INSERT INTO bot_admins \
                    (name, id) VALUES (%s, %s)  ON CONFLICT DO NOTHING;"
    elif table == "regions":
        format_str = "INSERT INTO regions \
                     (name) VALUES (%s);"
    elif table == "errors":
        timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
        format_str = "INSERT INTO errors\
                      (id, error, time) \
                       VALUES (%s, %s, %s)"
    else:
        log.error("Table not found.")
        return "error"
    try:
        if table == "schools":
            cursor.execute(format_str,
                           (data[0], data[1],
                            data[2], data[3],
                            data[4], data[5]))
        elif table == "bot_admins":
            cursor.execute(format_str,
                           (data[0], data[1]))
        elif table == "regions":
            cursor.execute(format_str,
                           (data))
        elif table == "errors":
            cursor.execute(format_str,
                           (data[0], data[1], timestamp))
        connection.commit()
        return None
    except Exception as e:  # pylint: disable=broad-except
        log.error("Error: {}".format(e))
        cursor.execute("ROLLBACK")
        return "error"


def fetch(table: str, ident: str):
    "Retrives ident from the table of choice."
    format_str = "SELECT %s FROM %s;"
    cursor.execute(format_str, (AsIs(ident),
                                AsIs(table)))
    fetched = cursor.fetchall()
    if ident == "*" or ident.find(",") != -1:
        result = fetched
    else:
        result = []
        for _, x in enumerate(fetched):
            result.append(x[0])
    return result


def update(table: str, ident: str, where: str, new_value: str):
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
    except psycopg2.Error as e:
        print(e)
        cursor.execute("ROLLBACK")


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
    except psycopg2.Error as pye:
        print(pye)
        cursor.execute("ROLLBACK")
