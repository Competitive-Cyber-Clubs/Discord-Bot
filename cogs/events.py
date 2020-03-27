"""Cog that manageages events"""
import discord
from discord.ext import commands


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
        await member.send("Welcome to the Competitive Cyber Clubs Discord Server.")  # noqa: E501 pylint: disable=line-too-long
