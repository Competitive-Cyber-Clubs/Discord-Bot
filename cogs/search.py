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
        `bot` `discord.commands.Bot` -- The bot class that deals with all the commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="validate-school")
    async def validate_school(self, ctx, *, school: str):
        """validate_school
        ---

        Validates school name. Only returns true or false.

        Arguments:
            ctx {discord.ext.commands.Context} -- Context of the command.
            school {str} -- Name of the school the user wants to validate.
        """
        await ctx.send(await utils.school_check(school))

    @commands.command(name="search-school")
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
            await ctx.send(
                "Please refine your search as {} returns a lot of results ".format(ctx.args()))
            return
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
        msg = ""
        for item in schools:
            msg += item + "\n"
        if len(msg) >= 2000:
            list_of_msgs = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
            for x in list_of_msgs:
                await ctx.send(x)
            return
        await ctx.send(msg)
