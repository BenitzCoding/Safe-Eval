import os
import io
import re
import time
import contextlib
import discord
import async_timeout
import asyncio
import multiprocessing

from async_timeout import timeout
from discord.ext import commands

ESCAPE_REGEX = re.compile("[`\u202E\u200B]{3,}")

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
		DISALLOWED_ENTITIES = ["while", ".close(", "new_event_loop(", "get_event_loop(", ".stop(", "importrequests", "__import__", "importos", "importsys", "importdiscord", "os.", ".getenv", "importsubprocess", "exec(", ".logout", "bot.", "eval(", ".get_event_loop(", ".create_task(", "(ctx)", "importimportlib", ".system("]
		code = code.replace(" ", "")
		code = code.replace("	", "")
		if "for" in code:
			nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
			l = list(code)
			array = []
			for char in l:
				if char in nums:
					array.append(int(char))
			str = ""
			for char in array:
				str += f"{char}"
			if int(str) > 480:
				return "MALICIOUS CODE DETECTED"
		for ENTITIES in DISALLOWED_ENTITIES:
			if ENTITIES in code.lower():
				return "MALICIOUS CODE DETECTED"

	def evaluation_task(self, ctx, code):
		if match := re.fullmatch(r"(?:\n*)?`(?:``(?:py(?:thon)?\n)?((?:.|\n)*)``|(.*))`", code, re.DOTALL):
			code = match.group(1) if match.group(1) else match.group(2)
			str_obj = io.StringIO()  # Retrieves a stream of data
			try:
				with contextlib.redirect_stdout(str_obj):
					exec(code)

				output = str_obj.getvalue()
				truncated = False
				lines = output.count("\n")

				if lines > 0:
					output = [f"{i:02d} | {line}" for i, line in enumerate(output.split('\n'), 1)]
					output = output[:-1]
					output = output[:11]  # Limiting to only 11 lines
					output = "\n".join(output)

				if lines > 10:
					truncated = True
					if len(output) >= 1000:
						output = f"{output[:1000]}\n... (truncated - too long, too many lines)"
					else:
						output = f"{output}\n... (truncated - too many lines)"
				
				elif len(output) >= 1000:
					truncated = True
					output = f"{output[:1000]}\n... (truncated - too long)"

				if ESCAPE_REGEX.findall(output):
					return f"{ctx.author.mention} :no_entry_sign: Code block escape attempt detected; will not output result"

			except Exception as e:
				return f"{ctx.author.mention} ❌ Your code completed with execution code 1\n```\n{e.__class__.__name__}: {e}\n```"
			if output == "":
				return f"{ctx.author.mention} ⚠ Your code completed with execution code 0\n```\n[No Output]\n```"
			return f"{ctx.author.mention} ✅ Your code completed with execution code 0\n```\n{output}\n```"

	@commands.command(name='eval', aliases=["e"])
	async def eval(self, ctx, *, command=None):
		async with timeout(2):
			if await self.MALICIOUS_INJECTION_CHECK(command) == "MALICIOUS CODE DETECTED":
				await ctx.send(f"{ctx.author.mention} :no_entry_sign: Your code wasn't proccessed due to security measures.")
				return
			try:
				p = multiprocessing.Process(target=self.evaluation_task(ctx, command))
				p.start()
				p.join(2)
				if p.is_alive():
					p.terminate()
					return await ctx.send(f"⚠ Your code completed with execution code 2\n```\n[Timed Out]\n```")
				else:
					return await ctx.send(self.evaluation_task(ctx, command))
			except TimeoutError:
				return await ctx.send(f"⚠ Your code completed with execution code 2\n```\n[Timed Out]\n```")
			return await ctx.send(self.evaluation_task(ctx, command))
			embed = discord.Embed(description="Error: Invalid format", color=0xED2525)
			return await ctx.send(embed=embed)

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		print(err)
		return await ctx.send(f"⚠ Your code completed with execution code 2\n```\n[Timed Out]\n```")


def setup(bot):
	bot.add_cog(Eval(bot))