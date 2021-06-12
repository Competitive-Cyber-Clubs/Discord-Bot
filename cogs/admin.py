"""Cog that has the admin features"""
import logging
from datetime import datetime
import discord.utils
from discord.ext import commands
import utils


log = logging.getLogger("bot")


class AdminCog(commands.Cog, name="Admin"):
    """AdminCog
    ---

    Cog that contains the commands for admin functions.

    Commands:
    ---
        `list-admins`: Sends a message that contain a list of the bot admin users.
        `am-admin`: Returns true of false depending on if the user is in the bot_admins table.
        `add-admin`: Add a user to the bot admin table.
        `add-admin-channel`: Add the channel that it was called in to the admin_channel table.
        `reload-extension`: Reloads the extensions names.
        `update-list`: Updates the list of schools

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        """cog_check
        ---

        cog_check is set for the whole cog. Which makes all the commands in health admin only.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.

        Returns:
            bool -- True if the user in the bot admins
        """
        return await utils.check_admin(ctx)

    @commands.command(
        name="list-admins",
        aliases=["ladmins", "ladmin"],
        help="List users that are bot admins",
    )
    async def list_admins(self, ctx: commands.Context):
        """List-admins
        ---
        Command that returns a list of the users that are in the bot_admin table.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        fetched = [x for x in await utils.fetch("bot_admins", "name") if x != "CCC-Dev-Bot"]
        embed = await utils.make_embed(ctx, send=False, title="Bot Admins:")
        admins = ""
        for admin in fetched:
            admins += "- {} \n".format(admin)
        embed.add_field(name="Admins", value=admins, inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        name="check-admin",
        aliases=["cadmin", "am-admin"],
        help="Tells you if you are a bot admin",
    )
    async def check_admin(self, ctx: commands.Context):
        """Check Admin
        ---

        Tells the user if they are in the bot admin table. Only return true or false.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        await utils.make_embed(ctx, title=await utils.check_admin(ctx))

    @commands.command(name="add-admin", help="Adds <user> to the bot admins table.")
    @commands.check(utils.check_admin)
    async def add_admin(self, ctx: commands.Context, *, user: discord.Member):
        """Add-Admin
        ---

        Adds `user` to the bot admin table.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
            user {str} -- The name of the user that you want to add to the bot_admin table
        """
        new_admin = discord.utils.get(ctx.guild.members, name=user)
        if new_admin:
            log.info("{} added new admin {}".format(ctx.author.display_name, user.display_name))
            await utils.insert("bot_admins", [new_admin.name, new_admin.id])
            await utils.make_embed(
                ctx, color="28b463", title="User: {} is now an admin.".format(new_admin)
            )
        else:
            await utils.error_message(ctx, "User not found.")

    @commands.command(name="add-admin-channel", help="Marks the channel as an admin channel")
    @commands.guild_only()
    @commands.check(utils.check_admin)
    async def add_admin_channel(self, ctx: commands.Context, log_status=False):
        """add-admin-channel
        ---

        Adds the channel where the command was run to the admin_channel table.
        By default it sets logging as false.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.

        Keyword Arguments:
        ---
            log_status {bool} -- [If the channel is for logging all users] (default: {False})
        """
        log_status = bool(log_status)
        await utils.insert("admin_channels", [ctx.channel.name, ctx.channel.id, log_status])
        await utils.make_embed(
            ctx,
            color="28b463",
            title="Admin Channel Success",
            description="Channel has been added with log status: {}".format(log_status),
        )

    @commands.command(name="reload-extension", help="reloads <extension>")
    async def reload_extension(self, ctx: commands.Context, extension: str):
        """reload_extension
        ---

        Command that reloads an extension.

        Arguments:
            ctx {discord.ext.commands.Context} -- Context of the command.
            extension {str} -- extension to reload
        """
        self.bot.reload_extension(extension)
        await utils.make_embed(ctx, color="28b463", title="Reloaded", description=extension)

    @commands.command(name="update-list", help="Updates the school_list.csv")
    async def refresh_list(self, ctx: commands.Context):
        """refresh_list
        ---

        Arguments:
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        await utils.update_list(self.bot, True)
        self.bot.list_updated = datetime.utcnow()
        await ctx.send("List updated")


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(AdminCog(bot))
