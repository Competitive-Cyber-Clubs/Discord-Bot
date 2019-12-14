import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


def create():
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
    if table == "School":
        for i in data:
            format_str = """INSERT OR IGNORE INTO {choice}\
                (school, color, region, added_by)""".format(choice=table)
            try:
                cursor.execute(format_str, (i[0], i[1]))
                connection.commit()
            except Exception as e:
                log.error(e)


def fetch(table, ident):  # Gets the data from the database
    cursor.execute(
        "SELECT {ident} FROM {table}".format(
            table=table, ident=ident))
    fetched = cursor.fetchall()
    if ident == "*":
        result = fetched
    # For items which are not selecting every column
    else:
        result = []
        for i in range(len(fetched)):
            # Gets all the first values and makes them into a list
            result.append(fetched[i][0])
    return result
