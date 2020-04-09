"""Schools commands for bot"""
import asyncio
import random
import logging
import discord
from discord.ext import commands
import utils


class SchoolCog(commands.Cog, name="Schools"):
    """SchoolCog
    ---

    Cog that deal with the school commands as well as the searching commands.

    Commands:
    ---
        `list-schools`: List all the available school roles that are joinable.
        `import-school`: Allows admin to import current roles into schools. *WIP*
        `join-school`: Allows users to join any available school role.
        `add-school`: Command that allows users to create their own school.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot

    Raises:
    ---
        utils.FailedReactionCheck: Custom exception if the reaction check fails.
    """
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("bot")

    @commands.command(name="list-schools",
                      help="Gets list of current schools")
    async def list_schools(self, ctx):
        """list-schools
        ---

        Lists current schools in the database. Message is a embed that has a random color with the
        list of all schools.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        fetched = sorted(await utils.fetch("schools", "school"), key=str.lower)
        if len(fetched) == 0:
            await ctx.send("There are no schools to join.")
            return
        schools = ""
        embed = await utils.make_embed(ctx, title="Available schools to join:",
                                       description="Use `$join-school` to join")
        for item in fetched:
            schools += "- {} \n".format(item)
        embed.add_field(name="Schools", value=schools, inline=False)
        embed.set_footer(text="If your school is not in the list, use `$help add-school`")
        await ctx.send(embed=embed)

    @commands.command(name="import-school",
                      help="Admin Only Feature")
    @commands.check(utils.check_admin)
    async def import_school(self, ctx, *, school_name: str):
        """import-school
        ---

        Allows admins to import existing roles as schools.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            school_name {str} -- Name of the school role to import.
        """
        srole = discord.utils.get(ctx.guild.roles, name=school_name)
        if srole.name in await utils.fetch("schools", "school"):
            embed = await utils.make_embed(ctx, "FF0000", title="That school already exists.")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Please enter the region for the school.")
            try:
                region = self.bot.wait_for('message', timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send("Took too long.")
                return
            new_school = [school_name, region.content, srole.color,  # pylint: disable=no-member
                          "Imported", "Imported"]
            status = await utils.insert("schools", new_school)
            if status == "error":
                embed = await utils.make_embed(ctx, color="FF0000",
                                               title="There was an error importing the school.")
            else:
                embed = await utils.make_embed(ctx, color="28b463",
                                               title="Region has been created")
            await ctx.send(embed=embed)

    @commands.command(name="join-school",
                      help="Joins a schools.")
    @commands.has_role("new")
    async def join_school(self, ctx, *, school_name: str):
        """join-school
        ---

        Enables users to join a school role. school_name arguments is not to be quote seperated.
        Users are required to have the role "new". Users will be assigned the school role, region
        role and "verified" role. They will lose their "new" role.


        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            school_name {str} -- Name of the school the user wants to join.
        """
        user = ctx.message.author
        db_entry = await utils.fetch("schools", "school, region")
        try:
            entries = [x for x in db_entry if x[0] == school_name][0]
        except IndexError:
            error_embed = await utils.make_embed(ctx, "FF0000", title="Error:",
                                                 description="School could not be found.")
            await ctx.send(embed=error_embed)
            return
        else:
            to_add = []
            for item in (*entries, "verified"):
                to_add.append(discord.utils.get(ctx.guild.roles, name=item))
            if None in to_add:
                title = "The school you select does not have valid role."
                embed = await utils.make_embed(ctx, "FF0000",
                                               title=title)
                await ctx.send(embed=embed)
                self.log.warning("{} tried to join {}. Only roles found: {}".format(ctx.author.name,
                                                                                    school_name,
                                                                                    to_add))
            else:
                await user.add_roles(
                    *to_add,
                    reason="{u} joined {s}".format(u=user.name, s=entries[0])
                )
                await user.remove_roles(
                    discord.utils.get(ctx.guild.roles, name="new"),
                    reason="{u} joined {s}".format(u=user.name, s=entries[0])
                )
                msg = "School assigned: {}".format(entries[0])
                await ctx.author.send(embed=await utils.make_embed(ctx, "28b463",
                                                                   title=msg))

    @commands.command(name="add-school",
                      help="Adds a new school and makes a role for it .",
                      description="Creates a new school")
    @commands.has_role("new")
    async def add_school(self, ctx, *, school_name: str):  # noqa: E501 pylint: disable=too-many-branches,line-too-long
        """add_school
        ---

        Enables users to create a school role. They are required to have the role "new". Schools
        will automatically be assigned a region based on the schools.csv in utils.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            school_name {str} -- Name of the school the user wants to join.

        Raises:
        ---
            utils.FailedReactionCheck: Expection is raised if the reaction check does not validate.
        """
        if not await utils.school_check(school_name):
            await ctx.send(embed=await utils.make_embed(
                ctx, "FF0000", title="Error: School name not valid."))
            return
        r_regions = await utils.fetch("regions", "name")
        region = await utils.region_select(school_name)
        if region not in r_regions:
            # No region map error
            self.log.error("There is no region map for {}, region: {}, {}".format(school_name,
                                                                                  region,
                                                                                  r_regions))
            await ctx.send(embed=await utils.make_embed(
                ctx, "FF0000", title="Error: There is no region mapped"))
            return
        prompt_embed = await utils.make_embed(
            ctx, title="You are about to create a new school: {}.".format(school_name),
            description="React  👍  to confirm.")
        await ctx.send(embed=prompt_embed)
        # Gives the user 30 seconds to add the reaction '👍' to the message.
        try:
            reactions, user = await self.bot.wait_for("reaction_add", timeout=30)
            if not await utils.check_react(ctx, user, reactions, "👍"):
                raise utils.FailedReactionCheck
        except asyncio.TimeoutError:
            await ctx.send(embed=await utils.make_embed(ctx, "FF0000", title="Error:",
                                                        description="Timed out."))
        except utils.FailedReactionCheck:
            await ctx.send(embed=await utils.make_embed(ctx, "FF0000", title="Error:",
                                                        description="Most likely the wrong react was added or by the wrong user."))  # noqa: E501 pylint: disable=line-too-long
        else:
            color = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)  # nosec
            added_school = await ctx.guild.create_role(
                name=school_name,
                color=discord.Color(color),
                mentionable=True,
                hoist=False,
                reason="Added by {}".format(ctx.author.name))
            data = [school_name,
                    region,
                    color,
                    added_school.id,
                    (ctx.author.name+ctx.author.discriminator),
                    ctx.author.id]
            status = await utils.insert("schools", data)
            if status == "error":
                embed = await utils.make_embed(
                    ctx, "FF0000", title="Error",
                    description="There was an error with creating the role.")
                rrole = discord.utils.get(ctx.guild.roles, name=school_name)
                await rrole.delete(reason="Error in creation")
                self.log.warning("due to error with School Role creation.")
            else:
                success_msg = "School \"{}\" has been created in {} with color of 0x{}"\
                              .format(school_name, region, color)
                embed = await utils.make_embed(ctx, color=color, title="Success",
                                               description=success_msg)
            await ctx.send(embed=embed)
