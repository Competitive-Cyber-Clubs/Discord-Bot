import os
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
import datahandler

load_dotenv()

GUILD = os.getenv('DISCORD_GUILD')
TOKEN = os.getenv('DISCORD_TOKEN')

BOT_PREFIX = ("$", "!")


client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}'
    )


@client.command(name="ping")
async def ping(ctx):
    await ctx.send("pong")

client.run(TOKEN)
