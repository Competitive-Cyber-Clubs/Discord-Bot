"""Cog that manages events"""
import discord
from discord.ext import commands
import utils


class EventsCog(commands.Cog, name="Events"):
    """EventsCog

    Cog that manages the events

    Events:
        `on_member_join`: Triggered when a new member joins.
            The bot will send them a welcome PM.

        `on_member_remove`: Triggered when a member leaves.
            A message will be send to the loggin admin channels.

    Arguments:
        `bot` `discord.commands.Bot` -- The bot class that deals with all the commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """on_member_join

        Event is triggered when a new member joins. The member recives a welcome PM.
        The message content is pulled from the messages table and it needs a name of "welcome".

        Arguments:
            member {discord.Member} -- The member that joined
        """
        new_role = discord.utils.get(member.guild.roles, name="new")
        await member.add_roles(
            new_role,
            reason="{} joined the server".format(member.name))
        welcome_message = await utils.select("messages", "message", "name",
                                             "welcome").replace(r"\n", "\n")
        if welcome_message:
            await member.send(welcome_message)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """on_member_remove

        Event is triggered when a members leaves the server.
        There is a message that they left that is sent to all admin_logging channels.

        Arguments:
            member {discord.Member} -- The member that left
        """
        channel = self.bot.get_channel(await utils.select("admin_channels", "id", "log", "t"))
        await channel.send("{} user left".format(member.name))
