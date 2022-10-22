"""Schools commands for bot"""
import asyncio
import random
import discord
from discord.ext import commands
from bot import utils


class SchoolCog(commands.Cog, name="Schools"):
    """
    School Cog

    **Commands:**

        - `list-schools`: List all the available school roles that are joinable.

        - `import-school`: Allows admin to import current roles into schools.

        - `join-school`: Allows users to join any available school role.

        - `add-school`: Command that allows users to create their own school.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list-schools", help="Gets list of current schools")
    async def list_schools(self, ctx) -> None:
        """
        List schools

        Lists current schools in the database. Message is a embed that has a random color with the
        list of all schools.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :return: None
        """
        fetched = sorted(await utils.fetch("schools", "school"), key=str.lower)
        if len(fetched) == 0:
            return await utils.error_message(ctx, "No schools to join")
        await utils.list_message(
            ctx,
            fetched,
            title="Available schools to join:",
            footer="If your school is not in the list, use `$help add-school`",
        )

    @commands.command(name="import-school", help="Admin Only Feature")
    @commands.check(utils.check_admin)
    async def import_school(self, ctx, school_name: str, region: str) -> None:
        """
        Import school

        Allows admins to import existing roles as schools.

        :param ctx: Command context
        :param school_name: Name of school role
        :type school_name: str
        :param region: Region of the school
        :type region: str
        :return: None
        """
        school_role = discord.utils.get(ctx.guild.roles, name=school_name)
        if school_role.name in await utils.fetch("schools", "school"):
            await utils.error_message(ctx, "School role already exists")
        else:
            new_school = [
                school_name,
                region,
                school_role.color.value,
                school_role.id,  # noqa: E501 pylint: disable=no-member
                "Imported",
                self.bot.owner_id,
            ]
            status = await utils.insert("schools", new_school)
            if status == "error":
                await utils.error_message(ctx, "Error importing school")
            else:
                await utils.make_embed(ctx, color="28b463", title="School has been imported")

    @commands.command(name="join-school", help="Joins a schools.")
    @commands.has_role("new")
    async def join_school(self, ctx, *, school_name: str) -> None:
        """Join School

        Enables users to join a school role. school_name arguments is not to be quote separated.
        Users are required to have the role "new". Users will be assigned the school role, region
        role and "verified" role. They will lose their "new" role.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param school_name: Name of the school role
        :type school_name: str
        :return: None
        """
        user = ctx.message.author
        db_entry = await utils.select("schools", "school, region", "school", school_name)
        if len(db_entry) == 0:
            return await utils.error_message(
                ctx, "School could not be found.", title="Missing School:"
            )

        to_add = [discord.utils.get(ctx.guild.roles, name=x) for x in (school_name, "verified")]
        if None in to_add:
            await utils.error_message(ctx, "The school you select does not have valid role.")
            self.bot.log.warning(
                f"{ctx.author.name} tried to join {school_name}. Only roles found: {to_add}"
            )
        else:
            self.bot.log.debug(f"Adding roles: {to_add} to {user}")
            await user.add_roles(*to_add, reason=f"{user.name} joined {school_name}")
            await user.remove_roles(
                discord.utils.get(ctx.guild.roles, name="new"),
                reason=f"{user.name} joined {school_name}",
            )
            await ctx.author.send(
                embed=await utils.make_embed(
                    ctx,
                    "28b463",
                    send=False,
                    title=f"School assigned: {school_name}",
                )
            )
            await ctx.message.add_reaction("✅")

    @commands.command(name="admin-add-school")
    @commands.check(utils.check_admin)
    async def admin_add_school(self, ctx: commands.Context, *, school_name: str) -> None:
        """
        Admin Add school

        Enables admins to create a school roles.
        There is no error checking and it will not assign the newly created role

        :param ctx: Command Context
        :type ctx: discord.ext.commands.Context
        :param school_name: Name of school to join
        :type school_name: str
        :return: None
        """
        if not await utils.school_check(self.bot.school_list, school_name):
            return await utils.error_message(ctx, message="School name not valid.")

        if await utils.select("schools", "school", "school", school_name):
            self.bot.log.info(
                f"{ctx.author.name} attempted to create a duplicate role for {school_name}"
            )
            return await utils.error_message(
                ctx,
                f"School role for {school_name} already exists.\n"
                f"Use `?join-school {school_name}` to join it",
            )

        regions = await utils.fetch("regions", "name")
        region = await utils.region_select(self.bot.school_list, school_name)
        if region not in regions:
            # No region map error
            self.bot.log.error(
                f"There is no region map for {school_name}, region: {region}, regions{regions}"
            )
            return await utils.error_message(ctx, f"No region defined for {school_name}")

        color = int(f"0x{random.randint(0, 0xFFFFFF)}", 16)  # nosec
        added_school = await ctx.guild.create_role(
            name=school_name,
            color=discord.Color(color),
            mentionable=True,
            hoist=False,
            reason=f"Added by {ctx.author.name}",
        )
        data = [
            school_name,
            region,
            color,
            added_school.id,
            (ctx.author.name + ctx.author.discriminator),
            ctx.author.id,
        ]
        status = await utils.insert("schools", data)
        if status == "error":
            await utils.error_message(ctx, "There was an error with creating the role.")
            await added_school.delete(reason="Error in creation")
            self.bot.log.warning("Error with School Role creation.")
        else:
            success_msg = (
                f'School "{school_name}" has been created in {region} with color of 0x{color}'
            )
            await utils.make_embed(ctx, color=color, title="Success", description=success_msg)

    @commands.command(
        name="add-school",
        help="Adds a new school and makes a role for it.\n"
             "Only schools on the list are allowed to join.\n"
             "List: https://github.com/Competitive-Cyber-Clubs/School-List/blob/master/school_list.csv",
        description="Creates a new school",
    )
    @commands.has_role("new")
    async def add_school(
            self, ctx: commands.Context, *, school_name: str
    ) -> None:  # pylint: disable=too-many-branches
        """
        Add school

        Enables users to create a school role. They are required to have the role "new". Schools
        will automatically be assigned a region based on the school_list.csv in utils.

        **Raises:**

            utils.FailedReactionCheck: Exception is raised if the reaction check does not validate.

        :param ctx: Command Context
        :type ctx: discord.ext.commands.Context
        :param school_name: Name of school to join
        :type school_name: str
        :return: None
        """
        if not await utils.school_check(self.bot.school_list, school_name):
            return await utils.error_message(ctx, message="School name not valid.")

        if await utils.select("schools", "school", "school", school_name):
            self.bot.log.info(
                f"{ctx.author.name} attempted to create a duplicate role for {school_name}"
            )
            return await utils.error_message(
                ctx,
                f"School role for {school_name} already exists.\n"
                f"Use `?join-school {school_name}` to join it",
            )

        regions = await utils.fetch("regions", "name")
        region = await utils.region_select(self.bot.school_list, school_name)
        if region not in regions:
            # No region map error
            self.bot.log.error(
                f"There is no region map for {school_name}, region: {region}, regions: {regions}"
            )
            return await utils.error_message(ctx, f"No region defined for {school_name}")
        color = random.randint(0, 16777215)  # nosec
        await utils.make_embed(
            ctx,
            title=f"You are about to create a new school: {school_name}.",
            description="React 👍 to this message in 60 seconds to confirm.",
            color=color,
        )
        # Gives the member 60 seconds to add the reaction '👍' to the message.
        try:
            reactions, user = await self.bot.wait_for("reaction_add", timeout=60)
            if not await utils.check_react(ctx, user, reactions, "👍"):
                raise utils.FailedReactionCheck
        except asyncio.TimeoutError:
            await utils.error_message(
                ctx, "Timed out waiting for a reaction. Please reach to the message in 30 seconds"
            )
        except utils.FailedReactionCheck:
            await utils.error_message(ctx, "Wrong reaction added or added by the wrong member")
        else:
            added_school = await ctx.guild.create_role(
                name=school_name,
                color=discord.Color(color),
                mentionable=True,
                hoist=False,
                reason=f"Added by {ctx.author.name}",
            )
            data = [
                school_name,
                region,
                color,
                added_school.id,
                (ctx.author.name + ctx.author.discriminator),
                ctx.author.id,
            ]
            status = await utils.insert("schools", data)
            if status == "error":
                await utils.error_message(ctx, "There was an error with creating the role.")
                await added_school.delete(reason="Error in creation")
                self.bot.log.warning("Error with School Role creation.")
            else:
                success_msg = (
                    f'School "{school_name}" has been created in {region} with color of 0x{color}'
                )
                await utils.make_embed(ctx, color=color, title="Success", description=success_msg)
                await self.join_school(ctx=ctx, school_name=school_name)


async def setup(bot):
    """Needed for extension loading"""
    await bot.add_cog(SchoolCog(bot))
