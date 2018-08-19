# Import libraries
import asyncio
import discord
import requests

# Discord bot client
token = "" # Discord bot token goes here
clevertoken = "" # Cleverbot token goes here
cl = discord.Client()
u = {}
p = {}
cs = {}
s = 0

# Constants
mat1 = discord.User(id="224862746964000768")
server = discord.Server(id="369571978019078144")
roles = [discord.Role(id="389922207419072512", server=server), discord.Role(id="385788047146483714", server=server), discord.Role(id="389928722322554881", server=server)]
rolenames = ["Launchpadder", "Launchpad Creator", "Music Producer"]
r = ['1\N{COMBINING ENCLOSING KEYCAP}', '2\N{COMBINING ENCLOSING KEYCAP}', '3\N{COMBINING ENCLOSING KEYCAP}']
y = ['✅', '🚫']
prefix = "!"

# Strings
current = 'Your current roles are:'
apply = 'Which role would you like to apply for?'
submitted = ['Your application for', 'has been submitted!']
cant = "You are currently locked. You can't use that command right now."
reset = 'Locks have been reset!'
help = 'Available commands:\n```!help - shows this message\n!reset - resets all locks\n!role - apply for a role on the server```'
wants = ['wants to apply for the', 'role.']
yourapp = 'Your application for'
approved = 'has been approved! Enjoy :wink:'
rejected = 'has been rejected for the following reason:'
dmerror = 'You need to send that command from the mat1jaczyyy Server for me to be able to get your roles.'
link = 'https://discord.gg/gzTtTtD'
allroles = 'You cannot apply for any other roles at this time.'
why = 'Why tho?'
ty = 'Thanks.'
yt = 'Please drop a link to your YouTube channel or a YouTube video where you upload original Launchpad covers and project files, along with any additional information you believe might be necessary.'
sc = 'Please drop a link to your SoundCloud profile, YouTube channel or YouTube video where you upload original music, along with any additional information you believe might be necessary.'
additionalprefix = ' Additional info provided: '
unknown = 'Unknown command.'
dms = 'Check your DMs.'
trilogy = 'https://www.youtube.com/user/Trilogyyyyyy?sub_confirmation=1'

# Helper functions
def goodOrigin(channelName):
	return str(channelName) == "mat2jaczyyy" or str(channelName).startswith("Direct Message")

# Login message
@cl.event
async def on_ready():
	print('Logged in as ' + str(cl.user) + "\n------")

# Message handling
@cl.event
async def on_message(m):
	# If the bot heard the echo of its own voice
	if m.author == cl.user:
		return

	# Create user lock if non-existent
	if m.author not in u:
		u[m.author] = 0
	
	# Command list
	if m.content == prefix + 'help':
		# If asked in BOT channel
		if goodOrigin(m.channel):
			await cl.send_message(m.channel, help)
		# Asked elsewhere
		else:
			await cl.delete_message(m)
			await cl.send_message(m.author, help)
	
	# Reset user lock
	elif m.content == prefix + 'reset':
		# If not asked in BOT channel
		if not goodOrigin(m.channel):
			await cl.delete_message(m)
			await cl.send_message(m.author, reset)
		else:
			await cl.send_message(m.channel, reset)
		
		# Clear the lock
		u[m.author] = 0
	
	# Role application
	elif m.content == prefix + 'role':
		# If not asked in BOT channel
		if goodOrigin(m.channel):
			# If user locked
			if u[m.author] > 0:
				await cl.send_message(m.channel, cant)
				return
		
		# Asked elsewhere
		else:
			await cl.delete_message(m)
			# If user locked
			if u[m.author] > 0:
				await cl.send_message(m.author, cant)
				return
		
		# If mat1 doing shit while superlocked
		global s
		if m.author == mat1 and s > 0:
			await cl.send_message(m.author, cant)
			return
		
		# If sent in server BOT channel
		if str(m.channel) == "mat2jaczyyy":
			await cl.send_message(m.channel, dms)
				
		# Get user roles
		try:
			cr = m.author.roles
			
		# If user sent a DM
		except AttributeError:
			await cl.send_message(m.author, dmerror + '\n' + link)
			return
		
		# Check pending roles
		if m.author not in p:
			p[m.author] = []
		
		# Check if user has all roles
		c = []
		for i in cr:
			if i in roles:
				c.append(i)
		for i in p[m.author]:
			if i in roles:
				c.append(i)
				
		# Role status
		d = '\n'.join([str(i + 1) + ". " + rolenames[i] + (" " * (18 - len(rolenames[i]))) + "- " + ("Assigned" if roles[i] in cr else ("Pending" if roles[i] in p[m.author] else "Not assigned")) for i in range(len(roles))])
		await cl.send_message(m.author, current + '\n```' + d + "```")
		
		# Stop if user can't apply for other roles
		if len(c) == len(roles):
			await cl.send_message(m.author, allroles)
			return
		
		# Lock user
		u[m.author] = 1
		
		# Send options message
		t = [await cl.send_message(m.author, apply)]
		e = []
		for i in range(len(r)):
			if roles[i] not in c and roles[i] not in p[m.author]:
				await cl.add_reaction(t[0], r[i])
				e.append(r[i])
		
		# Wait for user response
		a = await cl.wait_for_reaction(e, message=t[0], user=m.author)
		sel = int(a.reaction.emoji[0]) - 1
		
		# Remove other reactions
		for i in e:
			await cl.remove_reaction(t[0], i, member=cl.user)
		
		# Reset handling
		if u[m.author] == 0:
			for i in e:
				await cl.remove_reaction(t[0], i, member=m.author)
			return
		
		# Launchpad Creator role additional info
		additional = prefix
		origin = ""
		if sel == 1:
			t.append(await cl.send_message(m.author, yt))
			while additional.startswith(prefix) or not origin.startswith("Direct Message"):
				response = await cl.wait_for_message(author=m.author)
				origin = str(response.channel)
				additional = response.content
				# Reset handling
				if u[m.author] == 0:
					return
		
		# Music Producer role additional info
		if sel == 2:
			t.append(await cl.send_message(m.author, sc))
			while additional.startswith(prefix) or not origin.startswith("Direct Message"):
				response = await cl.wait_for_message(author=m.author)
				origin = str(response.channel)
				additional = response.content
				# Reset handling
				if u[m.author] == 0:
					return
		
		# Application submitted
		await cl.send_message(m.author, submitted[0] + ' ' + rolenames[sel] + ' ' + submitted[1])
		p[m.author].append(roles[sel])
		
		# Unlock user
		u[m.author] = 0
		
		# Superlock mat1
		s += 1
		
		# Ask mat1 for giving the role to the person
		t.append(await cl.send_message(mat1, "@" + str(m.author) + ' ' + wants[0] + ' ' + rolenames[sel] + ' ' + wants[1] + ((additionalprefix + '```' + additional + '```') if additional != "!" else "")))
		for i in y:
			await cl.add_reaction(t[-1], i)
		
		# Wait for mat1 response			
		a = await cl.wait_for_reaction(y, message=t[-1], user=mat1)
		b = a.reaction.emoji
		
		for i in y:
			await cl.remove_reaction(t[-1], i, member=cl.user)
		
		# mat1 said yes
		if b == y[0]:
			# Assign role
			await cl.add_roles(m.author, roles[sel])
			
			# Alert user of assignment
			del p[m.author][p[m.author].index(roles[sel])]
			await cl.send_message(m.author, yourapp + ' ' + rolenames[sel] + ' ' + approved)
		
		# mat1 said no
		else:
			# Ask why
			await cl.send_message(mat1, why)
			reason = prefix
			origin = ""
			while reason.startswith(prefix) or not origin.startswith("Direct Message"):
				response = await cl.wait_for_message(author=mat1)
				origin = str(response.channel)
				reason = response.content
			
			# Alert user of rejection
			del p[m.author][p[m.author].index(roles[sel])]
			await cl.send_message(m.author, yourapp + ' ' + rolenames[sel] + ' ' + rejected + ' ```' + reason + '```')
		
		# Unlock mat1
		await cl.send_message(mat1, ty)
		s += -1
	
	# Unknown/misspelled command
	elif m.content.startswith(prefix):
		if goodOrigin(m.channel):
			await cl.send_message(m.channel, unknown + '\n' + help)
	
	# Subscribe to Trilogy
	elif "subscribe to trilogy" in m.content.lower() and not "unsubscribe" in m.content.lower():
		await cl.send_message(m.channel, trilogy)
			
	# Engage cleverbot response
	elif (str(m.channel).startswith("Direct Message") or (str(m.channel) == "mat2jaczyyy" and cl.user in m.mentions)) and u[m.author] == 0:
		# If previous conversation does not exist
		if str(m.channel) not in cs:
			cs[str(m.channel)] = ""
		
		# Get cleverbot response
		input = m.clean_content.replace("@mat2jaczyyy", "").replace("&", "and")
		req = requests.get('http://www.cleverbot.com/getreply?key=' + clevertoken + '&input=' + m.content + '&cs=' + cs[str(m.channel)]).json()
		cs[str(m.channel)] = req['cs']
		
		# Send cleverbot response
		await cl.send_message(m.channel, ('' if str(m.channel).startswith("Direct Message") else (m.author.mention + ' ')) + req['output'])

# Run client
cl.run(token)