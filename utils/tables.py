"""List of tables that are created
---
    Tables:
    ---
        schools: Table for school roles.
            school {text}: name of the school
            region {text}: name of the region where the school is
            color {int}: hex code of the color **
            id {bigint}: Discord ID of the role
            added_by {text}: Username who created the school **
            added_by_id {bigint}: Discord ID of the user who created the school

        bot_admins: Table for users that are bot admins.
            id {bigint}: Discord ID of admin
            name {text}: username of the admin

        admin_channels: Table for discord channels that are for admin.
            name {text}: Name of the channel
            id {bigint}: Discord ID of the channel
            log {bool}: If the channel is a logging channel or not

        regions: Table for region roles
            name {text}: Name of the region
            id {bigint}: Discord ID of the role

        errors: Table of information about errors
            id {smallint}: ID for the error. Each number is random.
            message {text}: The message that was sent causing the error.
            command {text}: The command that was triggered to run
            error {text}: The error that occurred
            time {timestamp}: The time when the error occurred.
            ack {bool}: If the error has been acknowledged

        keys: Table for misc information stored.
            key {text}: Name of the value
            value {text}: The value

        messages: Table for storing messages
            name {text}: Name of the messssage
            message {text}: Content of the message

        reports: Table for reports
            id {int}: ID of the report
            name {text}: Discord user name of reporter
            name_id {bigint}: Discord user ID reporter
            message {text}: Text of the report
            time {timestamp}: Time of the report
"""
tables = [
    """
CREATE TABLE IF NOT EXISTS schools(
school text UNIQUE NOT NULL DEFAULT '',
region text NOT NULL DEFAULT '',
color int NOT NULL DEFAULT '0',
id bigint NOT NULL DEFAULT '0',
added_by text NOT NULL DEFAULT '',
added_by_id bigint NOT NULL DEFAULT '0',
PRIMARY KEY (school)
);""",
    """
CREATE TABLE IF NOT EXISTS bot_admins(
id bigint UNIQUE NOT NULL DEFAULT '0',
name text NOT NULL DEFAULT '',
PRIMARY KEY (name)
);
""",
    """
CREATE TABLE IF NOT EXISTS admin_channels(
name text NOT NULL DEFAULT '',
id bigint NOT NULL DEFAULT '0',
log bool DEFAULT False,
PRIMARY KEY (name)
);
""",
    """
CREATE TABLE IF NOT EXISTS regions(
name text NOT NULL DEFAULT '',
id bigint NOT NULL DEFAULT '0',
PRIMARY KEY (name)
);
""",
    """
CREATE TABLE IF NOT EXISTS errors(
id smallint NOT NULL DEFAULT '0',
command text NOT NULL DEFAULT '',
message text NOT NULL DEFAULT '',
error text NOT NULL DEFAULT '',
time timestamptz NOT NULL,
ack bool NOT NULL DEFAULT FALSE,
PRIMARY KEY (id)
);""",
    """
CREATE TABLE IF NOT EXISTS keys(
key text NOT NULL DEFAULT '',
value text NOT NULL DEFAULT '',
PRIMARY KEY (key)
);""",
    """
CREATE TABLE IF NOT EXISTS messages(
name text NOT NULL DEFAULT '',
message text NOT NULL DEFAULT '',
PRIMARY KEY (name)
);""",
    """
CREATE TABLE IF NOT EXISTS reports(
id int NOT NULL DEFAULT '0',
name text NOT NULL DEFAULT '',
name_id bigint NOT NULL DEFAULT '0',
message text NOT NULL DEFAULT '',
time timestamptz NOT NULL,
PRIMARY KEY(id)
);""",
]
