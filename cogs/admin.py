"""Admin features cog for CCC Bot"""
import discord
from discord.ext import commands
import utils


class AdminCog(commands.Cog, name="Admin"):
    """Cog that holds the admin commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list-admins",
                      aliases=["ladmins", "ladmin"],
                      help="Gets a list of bot admins")
    async def ladmin(self, ctx):
        """Gets the name of bot admins"""
        fetched = [x for x in utils.fetch("bot_admins", "name") if x != "CCC-Dev-Bot"]
        msg = "Bot Admins:\n"
        for admin in fetched:
            msg += "- {} \n".format(admin)
        await ctx.send(msg)

    @commands.command(name="am-admin",
                      aliases=["cadmin"],
                      help="Tells you if you are admin")
    async def cadmin(self, ctx):
        """Tells the user if they are in the bot admin table"""
        await ctx.send(utils.check_admin(ctx))

    @commands.command(name="add-admin",
                      help="Adds a bot admin")
    @commands.check(utils.check_admin)
    async def aadmin(self, ctx, *, args: discord.Member):
        """Adds a new bot admin"""
        members = ctx.guild.members
        for i, x in enumerate(members):
            if args == x.name:
                utils.insert("bot_admins", (x.name, ctx.guild.members[i].id))
                await ctx.send("User is now an admin.")
                return
        await ctx.send("Error: User not found.")

    @commands.command(name="add-admin-channel")
    @commands.check(utils.check_admin)
    async def aachannel(self, ctx, log_status=False):
        """Adds the current channel to the admin channels"""
        log_status = bool(log_status)
        utils.insert("admin_channels", [
            ctx.channel.name,
            ctx.channel.id,
            log_status])
        await ctx.send("Channel has been added with log status: {}".format(log_status))
