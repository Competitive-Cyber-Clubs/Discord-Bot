"""Cog that has the admin features"""
import discord.utils
from discord.ext import commands
import utils


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

    Arguments:
    ---
        `bot` `discord.commands.Bot` -- The bot class that deals with all the commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list-admins",
                      aliases=["ladmins", "ladmin"],
                      help="List users that are bot admins")
    async def list_admins(self, ctx):
        """List-admins
        ---
        Command that returns a list of the users that are in the bot_admin table.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        fetched = [x for x in await utils.fetch("bot_admins", "name") if x != "CCC-Dev-Bot"]
        msg = "Bot Admins:\n"
        for admin in fetched:
            msg += "- {} \n".format(admin)
        await ctx.send(msg)

    @commands.command(name="check-admin",
                      aliases=["cadmin", "am-admin"],
                      help="Tells you if you are a bot admin")
    async def check_admin(self, ctx):
        """Check Admin
        ---

        Tells the user if they are in the bot admin table. Only return true or false.

        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        await ctx.send(await utils.check_admin(ctx))

    @commands.command(name="add-admin",
                      help="Adds <user> to the bot admins table.")
    @commands.check(utils.check_admin)
    async def add_admin(self, ctx, *, user):
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
            await utils.insert("bot_admins", (new_admin.name, new_admin.id))
            await ctx.send("User: {} is now an admin.".format(new_admin))
            return
        await ctx.send("Error: User not found.")

    @commands.command(name="add-admin-channel", help="Marks the channel as an admin channel")
    @commands.guild_only()
    @commands.check(utils.check_admin)
    async def add_admin_channel(self, ctx, log_status=False):
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
        await utils.insert("admin_channels", [
            ctx.channel.name,
            ctx.channel.id,
            log_status])
        await ctx.send("Channel has been added with log status: {}".format(log_status))
