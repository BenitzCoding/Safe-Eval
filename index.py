import os

import discord

from discord.ext import commands

print("Loading up main file.\n\n")

def env(item):
    return os.getenv(f"{item}")

PREFIX = env('PREFIX')
bot = commands.AutoShardedBot(command_prefix=[ f"{PREFIX}", f"<@!{env('CLIENT_ID')}>", f"<@!{env('CLIENT_ID')}> " ])

bot.load_extension(f"eval")

bot.run("<Your Token>")