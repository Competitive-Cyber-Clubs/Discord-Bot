"""Cogs that handles errors"""
import logging
import random
from datetime import datetime
from discord.ext import commands
import utils


class ErrorsCog(commands.Cog, name="Errors"):
    """ErrorsCogs
    ---

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("bot")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """Reports errors to users"""
        if isinstance(error, (commands.errors.MissingRole, commands.errors.CheckFailure)):
            error_msg = "You do not have the correct role for this command."
        elif isinstance(error, commands.errors.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            error_msg = "`{}` has missing required arguments".format(ctx.message.content)
        elif isinstance(error, commands.errors.CommandError):
            errors = await utils.fetch("errors", "id")
            error_id = random.randint(1, 32767)  # nosec
            while error_id in errors:
                self.log.warning("Error ID had to be regenerated")
                error_id = random.randint(1, 32767)  # nosec

            error_info = [
                error_id,
                ctx.message.content,
                "COG: {} COMMAND: {}".format(ctx.command.cog.qualified_name, ctx.command.name),
                str(error),
                datetime.utcnow(),
            ]

            self.log.error(error_info)
            error_msg = (
                "There was a command error.\n"
                "Please report it for investigation.\n"
                "Error #{}".format(error_id)
            )
            await utils.insert("errors", error_info)
        else:
            errors = await utils.fetch("errors", "id")
            error_id = random.randint(1, 32767)  # nosec
            while error_id in errors:
                self.log.debug("Error ID had to be regenerated")
                error_id = random.randint(1, 32767)  # nosec

            self.log.error((error_id, error))
            error_msg = (
                "There was an unknown error.\n"
                "Please report it for investigation.\n"
                "Error #{}".format(error_id)
            )
            self.log.error("There was the following error: {}".format(error))
            error_info = [
                error_id,
                ctx.message.content,
                "COG: {} COMMAND: {}".format(ctx.command.cog.qualified_name, ctx.command.name),
                str(error),
                datetime.utcnow(),
            ]
            await utils.insert("errors", error_info)

        await utils.make_embed(ctx, "FF0000", title="Error:", description=error_msg)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(ErrorsCog(bot))
