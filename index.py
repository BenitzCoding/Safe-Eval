import os
import io
import re
import contextlib
import discord

from discord.ext import commands

def env(item):
	return os.getenv(f"{item}")

PREFIX = env('PREFIX')
bot = commands.AutoShardedBot(command_prefix=[ f"{PREFIX}" f"<@!{env('CLIENT_ID')}>", f"<@!{env('CLIENT_ID')}> " ])

@bot.event
async def on_ready():
	ACTIVE_GUILD_LIST = []
	for guild in bot.guilds:
		ACTIVE_GUILD_LIST.append(guild.name)
	print(f"----- Developed By Benitz Original#1317 -----\n\nCLIENT NAME: {bot.user.name}\nCLIENT ID: {bot.user.id}\nCLIENT OWNER: {env('OWNER_ID')}\nACTIVE SERVERS: {len(bot.guilds)}\nSERVER LIST: {ACTIVE_GUILD_LIST}\nSOURCE CODE: https://github.com/BenitzCoding/Safe-Eval")

async def MALICIOUS_INJECTION_CHECK(code):
	DISALLOWED_ENTITIES = ["importos", "importsys", "importdiscord"]
	code = code.replace(" ", "")
	code = code.replace("	", "")
	for ENTITIES in DISALLOWED_ENTITIES:
		if ENTITIES in code:
			await ctx.send(":no_entry_sign: Your code wasn't proccessed due to security measures.")
			return "MALICIOUS CODE DETECTED"

@bot.command(name='e', aliases=["eval"])
async def _e(ctx, *, command=None):
	
	if MALICIOUS_INJECTION_CHECK(command) == "MALICIOUS CODE DETECTED":
		return
	
	if match := re.fullmatch(r"(?:\n*)?`(?:``(?:py(?:thon)?\n)?((?:.|\n)*)``|(.*))`", command, re.DOTALL):
		code = match.group(1) if match.group(1) else match.group(2)
		str_obj = io.StringIO()  # Retrieves a stream of data
		try:
			with contextlib.redirect_stdout(str_obj):
				exec(code)
		except Exception as e:
			return await ctx.send(f"❌ Your code completed with execution code 1\n```\n{e.__class__.__name__}: {e}\n```")
		if str_obj.getvalue() == "":
			return await ctx.send(f"⚠ Your code completed with execution code 0\n```\n[No Output]\n```")
		return await ctx.send(f"✅ Your code completed with execution code 0\n```\n{str_obj.getvalue()}\n```")
	embed = discord.Embed(description="Error: Invalid format", color=0xED2525)
	return await ctx.send(embed=embed)

bot.run(f"{env('TOKEN')}")