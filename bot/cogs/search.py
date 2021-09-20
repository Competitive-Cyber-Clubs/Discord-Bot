"""Cog responsible for searching for schools and schools in state"""
from discord.ext import commands
from bot import utils


class SearchCog(commands.Cog, name="Search"):
    """
    Search Cog

    Cog that deals with searching for schools by name and by state.

    **Commands:**
        - `validate-school`: Allows users to see if the school they select is valid.

        - `search-school`: Allows users to search all valid schools.

        - `search-state`: Allows users to see all valid schools per state.

    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="check-school",
        help="Checks to see if <school> exists in the csv.\n" "Only returns True or False",
    )
    async def validate_school(self, ctx: commands.Context, *, school: str) -> None:
        """
        Validate school

        Validates school name. Only returns true or false.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param school: Name of school the member wants to validate.
        :type school: str
        :return: None
        """
        await utils.make_embed(
            ctx, title=str(await utils.school_check(self.bot.school_list, school))
        )

    @commands.command(
        name="search-school",
        aliases=["search-schools"],
        help="Search all schools for <school>.\n"
        "College, University, Community are blocked as they return a lot of results.\n"
        "The full list is at https://github.com/Competitive-Cyber-Clubs/School-List/blob/master/school_list.csv",  # noqa: E501 pylint: disable=line-too-long
    )
    async def search_school(self, ctx: commands.Context, *, school: str) -> None:
        """
        Search school

        Searches for a school based on the school arguments. It search the school.csv in utils
        as a list using the `in` statement.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param school: Part of the name the member wants to search for.
        :type school: str
        :return: None
        """
        blocked_words = [
            "college",
            "university",
            "community",
            "arts",
            "technology",
            "institute",
        ]
        if school.lower() in blocked_words:
            await utils.error_message(
                ctx,
                f"Please refine your search as '{school}' returns a lot of results.",
                title="Search Error",
            )
            return
        results = await utils.school_search(self.bot.school_list, school)
        created_roles = await utils.fetch("schools", "school")
        if not results:
            await utils.error_message(ctx, "No results found")
        else:
            for place, results_name in enumerate(results):
                results[place] = (
                    f"{results_name[0]} :: "
                    f"Role created: {await utils.TF_emoji(results_name in created_roles)}"
                )
            await utils.list_message(ctx, results, "Search Results:\n")

    @commands.command(name="search-state")
    async def search_state(self, ctx: commands.Context, *, state: str):
        """
        Search state

        Returns all schools in a state.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param state: Name of the state that the member wants to get schools from.
        :type state: str
        :return: None
        """
        state = state.strip("\"'")
        schools = await utils.state_list(self.bot.school_list, state)
        if not any(schools):
            await utils.error_message(ctx, message="No results found.")
            return
        await utils.list_message(ctx, schools, f"Schools in State '{state.title()}'")


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(SearchCog(bot))
