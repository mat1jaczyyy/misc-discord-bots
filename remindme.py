import asyncio
import discord

from humanfriendly import parse_timespan

token = "" # Discord bot token goes here

cl = discord.Client()

@cl.event
async def on_ready():
	print('Logged in as ' + str(cl.user) + "\n------")

# Message handling
@cl.event
async def on_message(m):
	if m.author == cl.user:
		return
	
	msg = m.content.split()
	
	if len(msg) == 0:
		return
	
	if msg[0] == "!remindme":
		await cl.send_message(m.channel, m.author.mention + ", I'll remind you ;)")
		
		try:
			await asyncio.sleep(parse_timespan(msg[1]))
			await cl.send_message(m.channel, m.author.mention + ", " + ' '.join(msg[2:]))
		
		except Exception as e:
			await cl.send_message(m.channel, m.author.mention + ", something went wrong.\n```" + str(e) + "```")	
		
cl.run(token)