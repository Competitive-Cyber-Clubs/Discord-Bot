"""Admin features cog for CCC Bot"""
from discord.ext import commands
import utils


class AdminCog(commands.Cog, name="Admin"):
    """Cog that holds the admin commands"""
    def __init__(self, bot, log):
        self.bot = bot
        self.log = log

    @commands.command(name="list-admins",
                      aliases=["ladmins", "ladmin"],
                      help="Gets a list of bot admins")
    async def ladmin(self, ctx):
        """Gets the name of bot admins"""
        fetched = utils.fetch("bot_admins", "name")
        await ctx.send(fetched)

    @commands.command(name="am-admin",
                      aliases=["cadmin"],
                      help="Tells you if you are admin")
    async def cadmin(self, ctx):
        """Tells the user if they are in the bot admin table"""
        await ctx.send(utils.check_admin(ctx))

    @commands.command(name="add-admin",
                      help="Adds a bot admin")
    @commands.check(utils.check_admin)
    async def aadmin(self, ctx, args):
        """Adds a new bot admin"""
        members = ctx.guild.members
        for i, x in enumerate(members):
            if args == x.name:
                utils.insert("bot_admins", (x.name, ctx.guild.members[i].id), self.log)
                await ctx.send("User is now an admin.")
                return
        await ctx.send("Error: User not found.")
