"""Cog that manages events"""
import discord
from discord.ext import commands
from bot import utils


class EventsCog(commands.Cog, name="Events"):
    """EventsCog
    ---

    Cog that manages the events

    Events:
    ---
        `on_member_join`: Triggered when a new member joins.
            The bot will send them a welcome PM.

        `on_member_remove`: Triggered when a member leaves.
            A message will be sent to the logging admin channels.

    Arguments:
    ---
        bot {discord.commands.Bot} -- The bot
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Member join event

        Event is triggered when a new member joins. The member receives a welcome PM.
        The message content is pulled from the messages table, and it needs a name of "welcome".
        Doesn't use utils.make_embed due to not having context.

        :param member: Member who joined
        :type member: discord.Member
        :return: None
        """
        new_role = discord.utils.get(member.guild.roles, name="new")
        await member.add_roles(new_role, reason="f{member.name} joined the server")
        welcome_message = await utils.select("messages", "message", "name", "welcome")
        if welcome_message:
            welcome_message = welcome_message[0].replace(r"\n", "\n")
            try:
                await member.send(
                    embed=discord.Embed(
                        title="Welcome to the server!",
                        description=welcome_message,
                        timestamp=member.joined_at,
                    )
                )
            except discord.Forbidden:
                pass

        channels = await utils.select("admin_channels", "id", "log", True)
        for channel in channels:
            await self.bot.get_channel(channel).send(
                embed=discord.Embed(
                    title="User Joined",
                    color=discord.Color(int("FF0000", 16)),
                    description=f"{member.name} joined the server",
                )
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """
        Member leave

        Event is triggered when a member leaves the server.
        There is a message that they left that is sent to all admin_logging channels.
        Doesn't use utils.make_embed due to not having context.

        :param member: Member who left
        :type member: discord.Member
        :return: None
        """
        channels = await utils.select("admin_channels", "id", "log", True)
        for channel in channels:
            await self.bot.get_channel(channel).send(
                embed=discord.Embed(
                    title="User left",
                    color=discord.Color(int("FF0000", 16)),
                    description=f"{member.name} member left",
                )
            )


async def setup(bot: commands.Bot) -> None:
    """Needed for extension loading"""
    await bot.add_cog(EventsCog(bot))
