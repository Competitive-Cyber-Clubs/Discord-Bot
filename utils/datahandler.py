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
added_by text NOT NULL DEFAULT '',
PRIMARY KEY (school)
);""", """
CREATE TABLE IF NOT EXISTS bot_admins (
name text NOT NULL DEFAULT '',
id int NOT NULL DEFAULT '',
PRIMARY KEY (name)
)
"""]
    for i in commands:
        cursor.execute(i)


def insert(table, data, log):
    "Adds data to existing tables"
    if table == "Schools":
        log.debug(data)
        format_str = """INSERT INTO {choice}
                (school, region, color, added_by) VALUES (?, ?, ?, ?)"""\
                .format(choice=table)
        try:
            cursor.execute(format_str,
                           (data[0], data[1], data[2], data[3]))
            connection.commit()
            return None
        except Exception as e:  # pylint: disable=broad-except
            log.error(e)
            return "error"
    else:
        return "error"


def fetch(table, ident):
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
