"""Schools commands for bot"""
import asyncio
import random
import discord
from discord.ext import commands
import utils


class SchoolCog(commands.Cog, name="Schools"):
    """Cog that deal with the school commands"""
    def __init__(self, bot, log):
        self.bot = bot
        self.log = log

    @commands.command(name="list-schools",
                      help="Gets list of current schools")
    async def list_schools(self, ctx):
        """Lists current schools in the database"""
        if ctx.author.id in utils.fetch("bot_admins", "id"):  # pylint: disable=no-else-return
            channel = self.bot.get_channel(utils.select("admin_channels", "id", "log", "f"))
            fetched = utils.fetch("schools", "school, region, added_by")
            school_list = "Schools | Region | Added By\n"
            for school in fetched:
                school_list += " | ".join(school) + "\n"
            await channel.send(school_list)
            return
        else:
            fetched = sorted(utils.fetch("schools", "school"), key=str.lower)
        if len(fetched) == 0:
            await ctx.send("There are no schools to join.")
            return
        schools = ""
        embed = discord.Embed(title="Available schools to join:",
                              description="Use `$join-school` to join",
                              color=int("0x%06x" % random.randint(0, 0xFFFFFF), 0),  # nosec
                              timestamp=ctx.message.created_at)
        for item in fetched:
            schools += "- {} \n".format(item)
        embed.add_field(name="Schools", value=schools, inline=False)
        embed.set_footer(text="If your school is not in the list, use `$help add-school`")
        await ctx.send(embed=embed)

    @commands.command(name="join-school",
                      help="Joins a schools.")
    @commands.has_role("new")
    async def joinschool(self, ctx, *, sname):
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

    @commands.command(name="import-school",
                      help="Admin Only Feature")
    @commands.check(utils.check_admin)
    async def ischool(self, ctx, sname):
        """Allows admins to import existing roles as schools"""
        srole = discord.utils.get(ctx.guild.roles, name=sname)
        if srole.name in utils.fetch("schools", "school"):
            await ctx.send("That school already exists.")
        else:
            await ctx.send("Please enter the region for the school.")
            try:
                region = self.bot.wait_for('message', timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send("Took too long.")
                return
            new_school = [sname, region.content, srole.color,  # pylint: disable=no-member
                          "Imported", "Imported"]
            status = utils.insert("schools", new_school)
            if status == "error":
                await ctx.send("There was an error importing the school.")

    @commands.command(name="add-school",
                      help="Adds a new school as a role.\n Takes up to 3 arguments space seperated: school, region, color. Only school and region are required.\n**Space seperated schools need to be added in quotes.**\nie: $add-school \"Champlain College\" NORTHEAST #00a9e0",  # noqa: E501 pylint: disable=line-too-long
                      description="Creates a new school")
    async def add_school(self, ctx, school_name: str, color: str = None):  # noqa: E501 pylint: disable=too-many-branches,line-too-long
        """Creates school"""
        if not await utils.school_check(school_name):
            await ctx.send("School name not valid")
            return
        r_regions = utils.fetch("regions", "name")
        region = await utils.region_select(school_name)
        region += " Region"
        if region not in r_regions:
            self.log.error("There is no region map for {}".format(school_name))
            await ctx.send("There is no region mapped. Please contact an admin")
            return
        if not color:
            color = int("0x%06x" % random.randint(0, 0xFFFFFF), 0)  # nosec
        else:
            if len(color) == 6:
                color = '0x{color}'.format(color=color)
            elif len(color) == 7:
                color = color.replace('#', '0x')
            try:
                color = int(color)
            except TypeError:
                await ctx.send("Error: Please submit your color as hex")
                return

        await ctx.send("You are about to create a new school: {}."
                       "\nReact  👍  to confirm.".format(school_name))
        try:
            reactions, user = await self.bot.wait_for("reaction_add", timeout=30)
            if not utils.check_react(ctx, user, reactions, "👍"):
                raise utils.FailedCheck
        except asyncio.TimeoutError:
            await ctx.send("Took to long please try again")
        except utils.FailedCheck:
            await ctx.send("There was an error in the check. Most likely the wrong react was added or by the wrong user.")  # noqa: E501 pylint: disable=line-too-long
        else:
            await ctx.guild.create_role(name=school_name, color=discord.Color(color),
                                        mentionable=True,
                                        hoist=False,
                                        reason="Added by {}".format(ctx.author.name))
            added_school = discord.utils.get(ctx.guild.roles, name=school_name)

            data = [school_name,
                    region,
                    color,
                    added_school.id,
                    (ctx.author.name+ctx.author.discriminator),
                    ctx.author.id]

            status = utils.insert("schools", data)
            if status == "error":
                await ctx.send("There was an error with creating the role.\n"
                               "Please reach out to a bot admin.")
                rrole = discord.utils.get(ctx.guild.roles, name=school_name)
                await rrole.delete(reason="Error in creation")
                self.log.warning("due to error with School Role creation.")
            else:
                await ctx.send(
                    "School \"{}\" has been created in {} with color of 0x{}"
                    .format(school_name, region, color)
                    )

    @commands.command(name="validate-school")
    async def validate(self, ctx, *, school):
        """Validates school name"""
        await ctx.send(await utils.school_check(school))

    @commands.command(name="search-school")
    async def school_search(self, ctx, *, school):
        """Searchs for a school"""
        async with ctx.typing():
            results = await utils.school_search(school)
            if not results:
                msg = "No results found."
            else:
                msg = "Search Results:\n"
                for item in results:
                    msg += "- {} \n".format(item)
            if len(msg) >= 2000:
                list_of_msgs = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
                for x in list_of_msgs:
                    await ctx.send(x)
                return
        await ctx.send(msg)

    @commands.command(name="state-search")
    async def state_search(self, ctx, *, school):
        """Returns all schools in a state"""
        schools = await utils.state_list(school)
        msg = ""
        for item in schools:
            msg += item + "\n"
        if len(msg) >= 2000:
            list_of_msgs = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
            for x in list_of_msgs:
                await ctx.send(x)
            return
        await ctx.send(msg)
