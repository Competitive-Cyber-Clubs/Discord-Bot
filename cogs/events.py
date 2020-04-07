"""Cog that manages events"""
import discord
from discord.ext import commands
import utils


class EventsCog(commands.Cog, name="Events"):
    """EventsCog
    ---

    Cog that manages the events

    Events:
    ---
        `on_member_join`: Triggered when a new member joins.
            The bot will send them a welcome PM.

        `on_member_remove`: Triggered when a member leaves.
            A message will be send to the loggin admin channels.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """on_member_join
        ---

        Event is triggered when a new member joins. The member recives a welcome PM.
        The message content is pulled from the messages table and it needs a name of "welcome".

        Arguments:
        ---
            member {discord.Member} -- The member that joined
        """
        new_role = discord.utils.get(member.guild.roles, name="new")
        await member.add_roles(
            new_role,
            reason="{} joined the server".format(member.name))
        welcome_message = await utils.select("messages", "message", "name", "welcome")
        if welcome_message:
            welcome_message = welcome_message[0].replace(r"\n", "\n")
            embed = discord.Embed(title="Welcome to the server!",
                                  description=welcome_message,
                                  timestamp=member.joined_at)
            await member.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """on_member_remove
        ---

        Event is triggered when a members leaves the server.
        There is a message that they left that is sent to all admin_logging channels.

        Arguments:
        ---
            member {discord.Member} -- The member that left
        """
        channels = await utils.select("admin_channels", "id", "log", "t")
        embed = await discord.Embed(title="User left",
                                    color=discord.Color(int("FF0000", 16)),
                                    description="{} user left".format(member.name))
        for channel in channels:
            to_send = self.bot.get_channel(channel)
            await to_send.send(embed=embed)
