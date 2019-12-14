"Handles all SQL data and tables"
import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


def create():
    "Creates tables if they do not exist at startup"
    commands = ["""
CREATE TABLE IF NOT EXISTS Schools (
school text NOT NULL DEFAULT '',
color text NOT NULL,
region text NOT NULL,
added_by text NOT NULL,
PRIMARY KEY (school)
);""", """
CREATE TABLE IF NOT EXISTS bot_admins (
admin text NOT NULL DEFAULT '',
PRIMARY KEY (admin)
)
"""]
    for i in commands:
        cursor.execute(i)


def insert(table, data, log):
    "Adds data to existing tables"
    if table == "School":
        for i in data:
            format_str = """INSERT OR IGNORE INTO {choice}\
                (school, color, region, added_by)""".format(choice=table)
            try:
                cursor.execute(format_str, (i[0], i[1]))
                connection.commit()
            except sqlite3.DatabaseError as e:
                log.error(e)


def fetch(table, ident):  # Gets the data from the database
    "Retrives data from tables"
    format_str = """SELECT {ident} FROM {table}""".\
                 format(table=table, ident=ident)
    cursor.execute(format_str)
    fetched = cursor.fetchall()
    if ident == "*":
        result = fetched
    # For items which are not selecting every column
    else:
        result = []
        for i, _ in enumerate(fetched):
            # Gets all the first values and makes them into a list
            result.append(fetched[i][0])
    return result
