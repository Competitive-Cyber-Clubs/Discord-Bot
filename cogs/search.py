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

    @commands.command(name="check-school",
                      help="Checks to see if <school> exists in the csv.")
    async def validate_school(self, ctx, *, school: str):
        """validate_school
        ---

        Validates school name. Only returns true or false.

        Arguments:
            ctx {discord.ext.commands.Context} -- Context of the command.
            school {str} -- Name of the school the user wants to validate.
        """
        embed = await utils.make_embed(ctx, title=str(await utils.school_check(school)))
        await ctx.send(embed=embed)

    @commands.command(name="search-school",
                      help="Search all schools for <school>.\nCollege, University, Community are blocked as they return a lot of results.")  # noqa: E501 pylint: disable=line-too-long
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
        rules = [school.lower() == "college",
                 school.lower() == "university",
                 school.lower() == "community"
                 ]
        if any(rules):
            embed = await utils.make_embed(ctx, title="Search error",
                                           description="Please refine your search as \"{}\" returns a lot of results ".format(school),  # noqa: E501 pylint: disable=line-too-long
                                           color="FF0000"
                                           )
            await ctx.send(embed=embed)
            return
        results = await utils.school_search(school)
        if len(results) == 0:
            await ctx.send("No results found.")
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
            await ctx.send("No results found.")
        else:
            title = "Schools in State '{}'".format(state)
            await utils.list_message(ctx, schools, title)
