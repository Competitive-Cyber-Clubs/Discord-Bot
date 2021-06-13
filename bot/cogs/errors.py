"""Cogs that handles errors"""
import logging
import random
from datetime import datetime

import discord
from discord.ext import commands
from bot import utils

log = logging.getLogger("bot")


class ErrorsCog(commands.Cog, name="Errors"):
    """ErrorsCogs
    ---

    The cog that handles all errors.

    Commands:
    ---
    `ack-error`: Acknowledge an error by ID


    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ack-error", help="Acknowledge an error to stop it from appearing")
    @commands.check(utils.check_admin)
    async def ack_error(self, ctx: commands.Context, error_id: str) -> None:
        """Ack Error

        Acknowledge an error to prevent it from appearing in the task

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param error_id: Id of the error
        :type error_id: str
        :return: None
        """
        error = await utils.select("errors", "id", "id", error_id)
        if not error:
            await ctx.send(f"Error {error_id} not found")
        else:
            await utils.update(
                table="errors",
                where_column="id",
                where_value=error_id,
                column="ack",
                new_value=True,
            )
            await ctx.send(f"Error {error_id} has been acknowledged")

    @commands.command(name="ack-all", help="Acknowledge all errors")
    @commands.check(utils.check_admin)
    async def ack_all(self, ctx: commands.Context) -> None:
        """Ack All

        Acknowledge all currently unacknowledged errors

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :return:  None
        """
        errors = await utils.select(
            table="errors", column="id", where_column="ack", where_value=False
        )
        if not errors:
            await ctx.send("No errors need acknowledging")
            return
        error_count = 0
        for error in errors:
            await utils.update(
                table="errors",
                where_column="id",
                where_value=error,
                column="ack",
                new_value=True,
            )
            log.debug(
                "Acknowledged error {} as part of bulk acknowledgement by {}".format(
                    error, ctx.author.display_name
                )
            )
            error_count += 1
        await ctx.send(
            (
                "All errors have been acknowledged."
                f"Total: {str(error_count)}\nError Numbers: {', '.join(map(str, errors))}"
            )
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        """Error report

        On error add it to the database and inform user of error

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param error: Error that was raised
        :type error: Exception
        :return: None
        """
        if isinstance(error, commands.DisabledCommand):
            await utils.error_message(ctx, message=f"{ctx.command} has been disabled.")
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
                return
            except discord.HTTPException:
                pass

        if isinstance(error, (commands.errors.MissingRole, commands.errors.CheckFailure)):
            error_msg = "You do not have the correct role for this command."
        elif isinstance(error, commands.errors.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            error_msg = f"`{ctx.message.content}` has missing required arguments"
        else:
            errors = await utils.fetch("errors", "id")
            error_id = random.randint(1, 32767)  # nosec
            while error_id in errors:
                log.warning("Error ID had to be regenerated")
                error_id = random.randint(1, 32767)  # nosec

            log.error((error_id, error))
            log.exception(error, exc_info=True)
            error_msg = (
                "There was an unknown error.\n"
                "Please report it for investigation.\n"
                "Error #{}".format(error_id)
            )
            log.error("There was the following error: {}".format(error))
            error_info = [
                error_id,
                ctx.message.content,
                f"COG: {ctx.command.cog.qualified_name} COMMAND: {ctx.command.name}",
                str(error),
                datetime.utcnow(),
                False,
            ]
            await utils.insert("errors", error_info)

        await utils.make_embed(ctx, "FF0000", title="Error:", description=error_msg)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(ErrorsCog(bot))
