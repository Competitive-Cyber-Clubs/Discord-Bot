"Handles all SQL data and tables"
import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


def create():
    "Creates tables if they do not exist at startup"
    commands = ["""
CREATE TABLE IF NOT EXISTS Schools (
school text NOT NULL DEFAULT '',
region text NOT NULL DEFAULT '',
color int NOT NULL DEFAULT '',
id int NOT NULL DEFAULT '',
added_by text NOT NULL DEFAULT '',
added_by_id int NOT NULL DEFAULT '',
PRIMARY KEY (school)
);""", """
CREATE TABLE IF NOT EXISTS bot_admins (
name text NOT NULL DEFAULT '',
id int NOT NULL DEFAULT '',
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS admin_channels (
name text NOT NULL DEFAULT '',
id int NOT NULL DEFAULT '',
PRIMARY KEY (name)
);
""", """
CREATE TABLE IF NOT EXISTS regions(
name text NOT NULL DEFAULT '',
PRIMARY KEY (name)
);"""]
    for i in commands:
        cursor.execute(i)


def insert(table: str, data: list, log=None):
    "Adds data to existing tables"
    if table == "Schools":
        format_str = """INSERT INTO Schools
                (school, region, color, id, added_by) VALUES (?, ?, ?, ?, ?)"""
    elif table == "bot_admins":
        format_str = """INSERT OR IGNORE INTO bot_admins
                    (name, id) VALUES (?, ?)"""
    elif table == "regions":
        format_str = """INSERT INTO regions
                     (name) VALUES (?)"""
    else:
        log.error("Table not found.")
        return "error"
    try:
        if table == "Schools":
            cursor.execute(format_str,
                           (data[0], data[1], data[2], data[3], data[4]))
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
        return "error"


def fetch(table: str, ident: str):
    "Retrives ident from the table of choice."
    format_str = """SELECT {ident} FROM {table}""".\
                 format(table=table, ident=ident)
    cursor.execute(format_str)
    fetched = cursor.fetchall()
    if ident == "*" or ident.find(",") != -1:
        result = fetched
    else:
        result = []
        for _, x in enumerate(fetched):
            result.append(x[0])
    return result
