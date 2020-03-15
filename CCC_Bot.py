"Main bot file"
import os
import logging
import sys
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import cogs
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


class FailedCheck(Exception):
    """Exception if react checks fail"""


def check_admin(ctx):
    """Checks to see if message author is in bot_admins"""
    returned = [int(id) for id in utils.fetch("bot_admins", "id")]
    return ctx.message.author.id in returned


def check_react(ctx, user, reaction):
    """Checks to see if the reaction is the one needed"""
    return user == ctx.author and str(reaction.emoji) == "👍"


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


client.add_cog(cogs.RegionCog(client, log))
client.add_cog(cogs.AdminCog(client, log))

@client.command(name="list-schools",
                help="Gets list of current schools")
async def list_schools(ctx):
    """Lists current schools in the database"""
    if ctx.author.id in utils.fetch("bot_admins", "id"):  # noqa: E501 pylint: disable=no-else-return,line-too-long
        fetched = utils.fetch("schools", "school, region, added_by")
        school_list = "Schools | Region | Added By\n"
        for school in fetched:
            school_list += " | ".join(school) + "\n"
        await ctx.send(school_list)
        await ctx.author.send(school_list)
        return
    else:
        fetched = utils.fetch("schools", "school")
    if len(fetched) == 0:
        await ctx.send("There are no schools to join.")
        return
    schools = "Available schools to join:\n"
    for item in fetched:
        schools += "- " + item + "\n"
    schools += "\nTo join your schools please use `$join-school \"<Your school name>\"`.\n**Please use quotes or it will not work**"  # noqa: E501 pylint: disable=line-too-long
    await ctx.send(schools)


@client.command(name="add-school",
                help="Creates a new school",
                description="Adds a new school as a role.\n Takes up to 3 arguments space seperated: school, region, color. Only school and region are required.\n**Space seperated schools need to be added in quotes.\nie: $add-school \"Champlain College\" NORTHEAST #00a9e0")  # noqa: E501 pylint: disable=line-too-long
async def add_school(ctx, *args):
    "Creates school"
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

    await ctx.send("You are about to create a new school: {}."
                   "\nReact  👍  to confirm.".format(args[0]))
    try:
        reactions, user = await client.wait_for("reaction_add", timeout=30)
        if not check_react(ctx, user, reactions):
            raise FailedCheck
    except asyncio.TimeoutError:
        await ctx.send("Took to long please try again")
    except FailedCheck:
        await ctx.send("There was an error in the check. Most likely the wrong react was added or by the wrong user.")  # noqa: E501 pylint: disable=line-too-long
    else:
        await ctx.guild.create_role(name=args[0], color=discord.Color(color),
                                    mentionable=True,
                                    hoist=False,
                                    reason="Added by {}".format(ctx.author.name))  # noqa: E501 pylint: disable=line-too-long
        added_school = discord.utils.get(ctx.guild.roles, name=args[0])

        data = [args[0],
                args[1],
                color,
                added_school.id,
                (ctx.author.name+ctx.author.discriminator),
                ctx.author.id]

        status = utils.insert("schools", data, log)
        if status == "error":
            await ctx.send("There was an error with creating the role.\n"
                           "Please reach out to a bot admin.")
            rrole = discord.utils.get(ctx.guild.roles, name=args[0])
            await rrole.delete(reason="Error in creation")
            log.warning("Role deleted, due to error with School Role creation.")  # noqa: E501 pylint: disable=line-too-long
        else:
            await ctx.send(
                "School \"{}\" has been created in {} region with color of 0x{}"  # noqa: E501 pylint: disable=line-too-long
                .format(args[0], args[1], color)
                )


@client.command(name="join-school",
                help="Joins a schools.")
@commands.has_role("new")
async def joinschool(ctx, sname):
    """Allows users to join a school"""
    user = ctx.message.author
    db_entry = utils.fetch("schools", "school, region")
    entries = [x for x in db_entry if x[0] == sname][0]
    if entries is None:
        await ctx.send("School could not be found.")
    else:
        roles = (*entries, "verified")
        to_add = []
        for item in roles:
            to_add.append(discord.utils.get(ctx.guild.roles, name=item))
        if None in to_add:
            await ctx.send("The school you select does not have valid role.")
        else:
            await user.add_roles(
                *to_add,
                reason="{u} joined {s}".format(u=user.name, s=entries[0])
            )
            await user.remove_roles(
                discord.utils.get(ctx.guild.roles, name="new"),
                reason="{u} joined {s}".format(u=user.name, s=entries[0])
            )
            await ctx.author.send("School assigned: {}".format(entries[0]))


@client.command(name="import-school",
                help="Admin Only Feature")
@commands.check(check_admin)
async def ischool(ctx, sname):
    """Allows admins to import existing roles as schools"""
    srole = discord.utils.get(ctx.guild.roles, name=sname)
    if srole.name in utils.fetch("schools", "school"):
        await ctx.send("That school already exists.")
    else:
        await ctx.send("Please enter the region for the school.")
        try:
            region = client.wait_for('message', timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send("Took too long.")
            return
        new_school = [sname, region.content, srole.color,
                      "Imported", "Imported"]
        status = utils.insert("schools", new_school, log)
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
    elif isinstance(error, commands.errors.CommandError):
        log.error(error)
        await ctx.send("There was a command error.\n"
                       "Please report it for investgation.")
    else:
        log.debug("There was the following error: {}".format(error))

client.run(TOKEN)
