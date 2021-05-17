import os
import io
import re
import time
import contextlib
import discord
import async_timeout
import asyncio

from multiprocessing import Process
from async_timeout import timeout
from discord.ext import commands
from itertools import count
from multiprocessing import Process

class Eval(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print("Loading Evaluation Code.\n\n")

	def env(self, item):
		return os.getenv(f"{item}")

	@commands.Cog.listener()
	async def on_ready(self):
		ACTIVE_GUILD_LIST = []
		for guild in self.bot.guilds:
			ACTIVE_GUILD_LIST.append(guild.name)
		print(f"----- Developed By Benitz Original#1317 -----\n\nCLIENT NAME: {self.bot.user.name}\nCLIENT ID: {self.bot.user.id}\nCLIENT OWNER: {self.env('OWNER_ID')}\nACTIVE SERVERS: {len(self.bot.guilds)}\nSERVER LIST: {ACTIVE_GUILD_LIST}\nSOURCE CODE: https://github.com/BenitzCoding/Safe-Eval\n\n----- Developed By Benitz Original#1317 -----")

	async def MALICIOUS_INJECTION_CHECK(self, code):
		DISALLOWED_ENTITIES = ["importrequests", "__import__", "importos", "importsys", "importdiscord", "os.", ".getenv", "importsubprocess", "exec(", ".logout", "bot.", "eval(", ".get_event_loop(", ".create_task(", "(ctx)", "importimportlib", ".system("]
		code = code.replace(" ", "")
		code = code.replace("	", "")
		for ENTITIES in DISALLOWED_ENTITIES:
			if ENTITIES in code.lower():
				return "MALICIOUS CODE DETECTED"

	async def evaluation_task(self, ctx, code):
		if match := re.fullmatch(r"(?:\n*)?`(?:``(?:py(?:thon)?\n)?((?:.|\n)*)``|(.*))`", code, re.DOTALL):
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

	@commands.command(name='eval', aliases=["e"])
	async def eval(self, ctx, *, command=None):
		async with timeout(2):
			if await self.MALICIOUS_INJECTION_CHECK(command) == "MALICIOUS CODE DETECTED":
				await ctx.send(":no_entry_sign: Your code wasn't proccessed due to security measures.")
				return
			try:
				await asyncio.wait_for(await self.evaluation_task(ctx, command), timeout=5)
			except asyncio.TimeoutError:
				return await ctx.send(f"⚠ Your code completed with execution code 2\n```\n[Timed Out]\n```")
			embed = discord.Embed(description="Error: Invalid format", color=0xED2525)
			return await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Eval(bot))