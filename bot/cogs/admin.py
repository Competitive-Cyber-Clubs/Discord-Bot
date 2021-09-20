"""Cog that has the admin features"""
import logging
from datetime import datetime
import discord.utils
from discord.ext import commands
from bot import utils

log = logging.getLogger("bot")


class AdminCog(commands.Cog, name="Admin"):
    """Admin cog

    Cog that contains the commands for admin functions.

    **Commands:**
        - `list-admins`: Sends a message that contain a list of the bot admin users.

        - `am-admin`: Returns true of false depending on if the member is in the bot_admins table.

        - `add-admin`: Add a member to the bot admin table.

        - `add-admin-channel`: Add the channel that it was called in to the admin_channel table.

        - `reload-extension`: Reloads the extensions names.

        - `update-list`: Updates the list of schools

    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        """Cog Check

        cog_check is set for the whole cog. Which makes all the commands in health admin only.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :return: User is a bot admin
        :rtype: bool
        """
        return await utils.check_admin(ctx)

    @commands.command(
        name="list-admins",
        aliases=["ladmins", "ladmin"],
        help="List users that are bot admins",
    )
    async def list_admins(self, ctx: commands.Context) -> None:
        """List Admins

        Command that returns a list of the users that are in the bot_admin table.

        :param ctx: Context of the command.
        :type ctx: discord.ext.commands.Context
        """
        fetched = [x for x in await utils.fetch("bot_admins", "name") if x != "CCC-Dev-Bot"]
        embed = await utils.make_embed(ctx, send=False, title="Bot Admins:")
        admins = ""
        for admin in fetched:
            admins += f"- {admin} \n"
        embed.add_field(name="Admins", value=admins, inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        name="check-admin",
        aliases=["cadmin", "am-admin"],
        help="Tells you if you are a bot admin",
    )
    async def check_admin(self, ctx: commands.Context) -> None:
        """
        Checks to see if the message author is in the bot_admins table
        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :return: None
        """
        await utils.make_embed(ctx, title=await utils.check_admin(ctx))

    @commands.command(name="add-admin", help="Adds <member> to the bot admins table.")
    @commands.check(utils.check_admin)
    async def add_admin(self, ctx: commands.Context, *, user: discord.Member) -> None:
        """Add Admin

        Adds **member** to the bot admin table.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param user: Name of the member to add to the bot_admin table
        :type user: discord.Member
        :return: None
        """
        new_admin = discord.utils.get(ctx.guild.members, name=user)
        if new_admin:
            log.info(f"{ctx.author.display_name} added new admin {user.display_name}")
            await utils.insert("bot_admins", [new_admin.name, new_admin.id])
            await utils.make_embed(ctx, color="28b463", title=f"User: {new_admin} is now an admin.")
        else:
            await utils.error_message(ctx, "User not found.")

    @commands.command(name="add-admin-channel", help="Marks the channel as an admin channel")
    @commands.guild_only()
    @commands.check(utils.check_admin)
    async def add_admin_channel(self, ctx: commands.Context, log_status: bool = False) -> None:
        """Add Admin Channel

        Adds the channel where the command was run to the admin_channel table.
        By default it sets logging as false.

        :param ctx: Command context
        :type ctx: discord.ext.commands.Context
        :param log_status: Channel is for logging all users
        :type log_status: bool
        :return: None
        """
        log_status = bool(log_status)
        await utils.insert("admin_channels", [ctx.channel.name, ctx.channel.id, log_status])
        await utils.make_embed(
            ctx,
            color="28b463",
            title="Admin Channel Success",
            description=f"Channel has been added with log status: {log_status}",
        )

    @commands.command(name="reload-extension", help="reloads <extension>")
    async def reload_extension(self, ctx: commands.Context, extension: str) -> None:
        """
        Reload Extension

        Command that reloads an extension.

        :param ctx: Context of the command.
        :type ctx: discord.ext.commands.Context
        :param extension: Extension to reload
        :type extension: str
        :return: None
        """
        self.bot.reload_extension(extension)
        await utils.make_embed(ctx, color="28b463", title="Reloaded", description=extension)

    @commands.command(name="update-list", help="Updates the school_list.csv")
    async def refresh_list(self, ctx: commands.Context) -> None:
        """Refresh list

        Refresh the school list.csv
        :param ctx: Context of the command
        :type ctx: discord.ext.commands.Context
        :return: None
        """
        await utils.update_list(self.bot, True)
        self.bot.list_updated = datetime.utcnow()
        await ctx.send("List updated")


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(AdminCog(bot))
