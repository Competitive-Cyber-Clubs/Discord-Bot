"Main bot file"
import os
import logging
import sys
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import utils


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_NAME = os.getenv('OWNER_NAME')
OWNER_ID = os.getenv('OWNER_ID')
log_level = os.getenv('LOG_LEVEL')
if not log_level:
    log_level = logging.DEBUG


utils.create()
log = utils.make_logger("bot", log_level)
log.info("Starting up")
log.debug("Using discord.py version: {} and Python version {}"
          .format(discord.__version__, sys.version[0:5]))


def check_admin(ctx):
    """Checks to see if message author is in bot_admins"""
    returned = [int(id) for id in utils.fetch("bot_admins", "id")]
    return ctx.message.author.id in returned


client = commands.Bot(command_prefix="$", owner_id=OWNER_ID)


@client.event
async def on_ready():
    "Startup which shows servers it has conencted to"

    log.info(
        '{} is connected to the following guild: '
        '{}'.format(client.user, client.guilds[0].name)
    )
    utils.insert("bot_admins", [OWNER_NAME, OWNER_ID], log)
    admin_role = discord.utils.get(client.guilds[0].roles, name="Admin")
    for admin in admin_role.members:
        utils.insert("bot_admins", [admin.name, admin.id], log)
    await client.change_presence(activity=discord.Activity(
        name='Here to help!', type=discord.ActivityType.playing))


@client.command(name="ping",
                help="Testing command that returns pong",
                description="Pong")
async def ping(ctx):
    "Simple command that replies pong to ping"
    log.debug("{} has sent ping.".format(ctx.author.name))
    await ctx.author.send("pong")
    await ctx.message.delete()


@client.command(name="list-admins",
                aliases=["ladmins", "ladmin"],
                help="Gets a list of bot admins")
async def ladmin(ctx):
    """Gets the name of bot admins"""
    fetched = utils.fetch("bot_admins", "name")
    await ctx.send(fetched)


@client.command(name="am-admin",
                aliases=["cadmin"],
                help="Tells you if you are admin")
async def cadmin(ctx):
    """Tells the user if they are in the bot admin table"""
    await ctx.send(check_admin(ctx))

@client.command(name="add-admin",
                help="Adds a bot admin")
@commands.check(check_admin)
async def aadmin(ctx, args):
    """Adds a new bot admin"""
    members = ctx.guild.members
    for i, x in enumerate(members):
        if args == x.name:
            utils.insert("bot_admins", (x.name, ctx.guild.members[i].id), log)
            await ctx.send("User is now an admin.")
            return
    await ctx.send("Error: User not found.")


@client.command(name="list-schools",
                help="Gets list of current schools")
async def list_schools(ctx):
    """Lists current schools in the database"""
    if ctx.author.id in utils.fetch("bot_admins", "id"):
        fetched = utils.fetch("Schools", "school, region, added_by")
        for school in fetched:
            # await ctx.send(" | ".join(school))
            await ctx.author.send(" ".join(school))
        return
    else:
        fetched = utils.fetch("Schools", "school")
    if len(fetched) == 0:
        await ctx.send("There are no schools to join.")
        return
    schools = "Available schools to join:\n"
    for item in fetched:
        schools += "- " + item[0] + "\n"
    schools += "\nTo join your schools please use *$join-school \"<Your school name>\"*.\n**Please use quotes or it will not work**"  # noqa: E501 pylint: disable=line-too-long
    await ctx.send(schools)


@client.command(name="add-school",
                help="Creates a new school",
                description="Adds a new school as a role.\n Takes up to 3 arguments space seperated: school, region, color. Only school and region are required.\n**Space seperated schools need to be added in quotes.\nie: $add-school \"Champlain College\" NORTHEAST #00a9e0")  # noqa: E501 pylint: disable=line-too-long
async def add_school(ctx, *args):
    "Creates school"
    log.debug(args)
    if len(args) < 2:
        await ctx.send("Error: The argument add-school "
                       "requires at least 2 arguments")
        return
    r_regions = utils.fetch("regions", "name")
    if args[1] not in r_regions:
        await ctx.send("Error: The region you have selected is not available.")
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
                                hoist=True,
                                reason="Added by {}".format(ctx.author.name))
    added_school = discord.utils.get(ctx.guild.roles, name=args[0])

    data = [args[0],
            args[1],
            color,
            added_school.id,
            (ctx.author.name+ctx.author.discriminator),
            ctx.author.id]

    status = utils.insert("Schools", data, log)
    log.debug("Add school status: {}".format(status))
    if status == "error":
        await ctx.send("There was an error with creating the role.\n"
                       "Please reach out to a bot admin.")
        rrole = discord.utils.get(ctx.guild.roles, name=args[0])
        await rrole.delete(reason="Error in creation")
        log.debug("Role deleted, due to error with School Role creation.")
    else:
        await ctx.send(
            "School \"{}\" has been created in {} region with color of 0x{}"
            .format(args[0], args[1], color)
            )


@client.command(name="join-school",
                help="Joins a schools.")
@commands.has_role("new")
async def joinschool(ctx, sname):
    """Allows users to join a school"""
    user = ctx.message.author
    db_entry = utils.fetch("Schools", "school, region")
    entries = [x for x in db_entry if x[0] == sname][0]
    if not entries:
        await ctx.send("Role could not be found.")
    else:
        await user.add_roles(
            discord.utils.get(ctx.guild.roles, name=entries[0]),
            discord.utils.get(ctx.guild.roles, name=entries[1]),
            discord.utils.get(ctx.guild.roles, name="verified"),
            reason="{u} joined {s}".format(u=user.name, s=entries[0])
        )
        await user.remove_roles(
            discord.utils.get(ctx.guild.roles, name="new"),
            reason="{u} joined {s}".format(u=user.name, s=entries[0])
        )
        await ctx.author.send("School assigned: {}".format(entries[0]))


@client.command(name="add-region",
                help="Adds regions")
@commands.check(check_admin)
async def addregion(ctx, region):
    """Allows admins to add regions"""
    status = utils.insert("regions", [region], log)
    if not status == "error":
        await ctx.send('Region has been created.')
    else:
        await ctx.send("There was an error creating the region.")


@client.command(name="list-regions",
                help="Lists available regions.")
@commands.check(check_admin)
async def listregion(ctx):
    """Admin command to lists the regions"""
    await ctx.send(utils.fetch("regions", "name"))


@client.command(name="import-school",
                help="Admin Only Feature")
@commands.check(check_admin)
async def ischool(ctx, sname):
    """Allows admins to import existing roles as schools"""
    srole = discord.utils.get(ctx.guild.roles, name=sname)
    if srole.name in utils.fetch("Schools", "school"):
        await ctx.send("That school already exists.")
    else:
        await ctx.send("Please enter the region for the school.")
        try:
            region = client.wait_for('message', timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send("Took too long.")
            return
        new_school = [sname, region.content, srole.colour,  # noqa: E501 pylint: disable=no-member
                      "Imported", "Imported"]
        status = utils.insert("Schools", new_school, log)
        if status == "error":
            await ctx.send("There was an error importing the school.")


@client.command(name="add-rank",
                help="Adds student, alumni or professor role.")
@commands.has_role("verified")
async def addrank(ctx, rank):
    """Allows users to set student, alumni or professor role."""
    user = ctx.message.author
    ranks = ["student", "professor", "alumni"]
    checked = [i for i in user.roles if i.name.lower() in ranks]
    if len(checked) > 0:
        await ctx.send("Error: You already have a rank.")
        return
    rank = discord.utils.get(ctx.guild.roles, name=rank)
    await user.add_roles(rank)
    await ctx.send("Rank assigned successfully")


@client.event
async def on_command_error(ctx, error):
    """Reports errors to users"""
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You do not have the correct role for this command.")

client.run(TOKEN)
