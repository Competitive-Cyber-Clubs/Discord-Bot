"Main bot file"
import os
import logging
import sys
import random
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
import utils


load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_NAME = os.getenv('OWNER_NAME')
OWNER_ID = os.getenv('OWNER_ID')


utils.datahandler.create()
log = utils.make_logger("bot", logging.DEBUG)
log.info("Starting up")
log.debug("Using discord.py version: {} and Python version {}"
          .format(discord.__version__, sys.version[0:5]))


def check_admin(ctx):
    """Checks to see if message author is in bot_admins"""
    return ctx.message.author.id in utils.fetch("bot_admins", "id")


client = Bot(command_prefix="$", owner_id=OWNER_ID)


@client.event
async def on_ready():
    "Startup which shows servers it has conencted to"
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    log.info(
        '{} is connected to the following guild: '
        '{}'.format(client.user, client.guilds[0].name)
    )
    utils.insert("bot_admins", [OWNER_NAME, OWNER_ID], log)
    await client.change_presence(activity=discord.Game(name='Here to help!'))


@client.command(name="ping",
                help="Testing command that returns pong",
                description="Pong")
async def ping(ctx):
    "Simple command that replies pong to ping"
    log.debug("{} has sent ping.".format(ctx.author.name))
    await ctx.send("pong")


@client.command(name="add-school",
                help="Creates a new school",
                description="Adds a new school as a role.\n"
                "Takes up to 3 arguments space seperated. "
                "They are school, region, color. "
                "Only school and region are required.\n"
                "ie: $add-school \"Champlain College\" NORTHEAST #00a9e0")
async def new_school(ctx, *args):
    "Creates school"
    log.debug(args)
    if len(args) < 2:
        await ctx.send("Error: The argument add-school "
                       "requires at least 2 arguments")
        return

    if len(args) < 3:
        color = int("0x%06x" % random.randint(0, 0xFFFFFF), 0)  # nosec
    else:
        if len(args[2]) == 6:
            color = '0x{color}'.format(color=args[2])
        elif len(args[2]) == 7:
            color = color.replace('#', '0x')
        else:
            color = args[2]
        try:
            color = int(args[2])
        except TypeError:
            await ctx.send("Error: Please submit your color as hex")

    await ctx.guild.create_role(name=args[0], color=discord.Color(color),
                                mentionable=True,
                                reason="Added by {}".format(ctx.author.name))
    added_school = discord.utils.get(ctx.guild.roles, name=args[0])

    data = [args[0],
            args[1],
            color,
            added_school.id,
            (ctx.author.name+ctx.author.discriminator),
            ctx.author.id]
    status = utils.insert("Schools", data, log)
    log.debug(status)
    if status == "error":
        await ctx.send("There was an error with creating the role.\n"
                       "Please reach out to a bot admin.")
        rrole = discord.utils.get(ctx.guild.roles, name=args[0])
        await rrole.delete(reason="Error in creation")
        log.debug("Role deleted")
    else:
        await ctx.send(
            "School \"{}\" has been created in {} region with color of 0x{}"
            .format(args[0], args[1], color)
            )

@client.command(name="list-schools",
                help="Gets list of current schools")
async def list_schools(ctx):
    """Lists current schools in the database"""
    if ctx.author.id in utils.fetch("bot_admins", "admin"):
        fetched = utils.fetch("Schools", "school, region")
    else:
        fetched = utils.fetch("Schools", "school")
    await ctx.send(fetched)

@client.command(name="list-admin",
                help="Gets a list of bot admins")
async def ladmin(ctx):
    """Gets the name of bot admins"""
    fetched = utils.fetch("bot_admins", "name")
    await ctx.send(fetched)


@client.command(name="add-admin",
                help="Adds a bot admin")
@discord.ext.commands.check(check_admin)
async def aadmin(ctx, args):
    """Adds a new bot admin"""
    members = ctx.guild.members
    for i, x in enumerate(members):
        if args == x.name:
            utils.insert("bot_admins", (x.name, ctx.guild.members[i].id), log)
            await ctx.send("User is now an admin.")
            break
    await ctx.send("Error: User not found.")


client.run(TOKEN)
