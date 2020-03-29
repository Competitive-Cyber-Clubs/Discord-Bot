"""Cog that manages events"""
import discord
from discord.ext import commands
import utils


class EventsCog(commands.Cog, name="Events"):
    """Cog that holds the events"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Runs when a new member joins"""
        new_role = discord.utils.get(member.guild.roles, name="new")
        await member.add_roles(
            new_role,
            reason="{} joined the server".format(member.name))
        welcome_message = utils.select("messages", "message", "name",
                                       "welcome").replace(r"\n", "\n")
        if welcome_message:
            await member.send(welcome_message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Runs when a member leaves"""
        channel = self.bot.get_channel(utils.select("admin_channels", "id", "log", "t"))
        await channel.send("{} user left".format(member.name))
