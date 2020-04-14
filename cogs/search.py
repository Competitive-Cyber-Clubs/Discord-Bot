"""Cog responsible for searching for schools and schools in state"""
from discord.ext import commands
import utils


class SearchCog(commands.Cog, name="Search"):
    """SearchCog
    ---

    Cog that deals with searching for schools by name and by state.

    Commands:
    ---
        `validate-school`: Allows users to see if the school they select is valid.
        `search-school`: Allows users to search all valid schools.
        `search-state`: Allows users to see all valid schools per state.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="check-school",
        help="Checks to see if <school> exists in the csv.\n"
             "Only returns True or False")
    async def validate_school(self, ctx, *, school: str):
        """validate_school
        ---

        Validates school name. Only returns true or false.

        Arguments:
            ctx {discord.ext.commands.Context} -- Context of the command.
            school {str} -- Name of the school the user wants to validate.
        """
        await utils.make_embed(ctx, title=str(await utils.school_check(school)))

    @commands.command(
        name="search-school",
        help="Search all schools for <school>.\n"
             "College, University, Community are blocked as they return a lot of results.\n"
             "The full list is at https://github.com/Competitive-Cyber-Clubs/Discord-Bot/blob/master/utils/schools.csv"   # noqa: E501 pylint: disable=line-too-long
        )
    async def search_school(self, ctx, *, school: str):
        """search-school
        ---

        Searches for a school based on the school arguments. It search the school.csv in utils
        as a list using the `in` statement.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            school {str} -- Part of the name the user wants to search for.
        """
        blocked_words = ["college", "university", "community",
                         "arts", "technology", "institute"]
        if school.lower() in blocked_words:
            return await utils.make_embed(ctx, title="Search error", color="FF0000",
                                          description="Please refine your search as \"{}\" returns a lot of results ".format(school),  # noqa: E501 pylint: disable=line-too-long
                                          )
        results = await utils.school_search(school)
        if len(results) == 0:
            await utils.make_embed(ctx, color="FF0000", title="No results found.")
        else:
            await utils.list_message(ctx, results, "Search Results:\n")

    @commands.command(name="search-state")
    async def search_state(self, ctx, *, state: str):
        """search_state
        ---

        Returns all schools in a state.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            state {str} -- Name of the state that the user wants to get schools from.
        """
        schools = await utils.state_list(state)
        if len(schools) == 0:
            await utils.make_embed(ctx, color="FF0000", title="No results found.")
        else:
            title = "Schools in State '{}'".format(state.title())
            await utils.list_message(ctx, schools, title)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(SearchCog(bot))
