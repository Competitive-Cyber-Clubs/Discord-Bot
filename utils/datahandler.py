"Handles all SQL data and tables"
import os
import psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    connection = psycopg2.connect(host=os.getenv("DB_HOST"),
                                  port=os.getenv("DB_PORT"),
                                  user=os.getenv("DB_USER"),
                                  password=os.getenv("DB_PASSWORD"),
                                  dbname=os.getenv("DB_NAME"))

else:
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor = connection.cursor()


def create():
    "Creates tables if they do not exist at startup"
    commands = ["""
CREATE TABLE IF NOT EXISTS schools (
school text NOT NULL DEFAULT '',
region text NOT NULL DEFAULT '',
color text NOT NULL DEFAULT ' ',
id bigint NOT NULL DEFAULT '0',
added_by text NOT NULL DEFAULT '',
added_by_id bigint NOT NULL DEFAULT '0',
PRIMARY KEY (school)
);""", """
CREATE TABLE IF NOT EXISTS bot_admins (
id bigint NOT NULL DEFAULT '0',
name text NOT NULL DEFAULT '',
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS admin_channels (
name text NOT NULL DEFAULT '',
id bigint NOT NULL DEFAULT '0',
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS regions(
name text NOT NULL DEFAULT '',
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
