import discord
from discord.ext import commands

# Your bot token here
TOKEN = 'YOUR_BOT_TOKEN'

# Intents (required for Discord.py 2.x)
intents = discord.Intents.default()
intents.messages = True

# Set up the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Simple in-memory state
user_states = {}

@bot.command(name='cpe')
async def cpe(ctx):
    user_states[ctx.author.id] = {'step': 'name'}
    await ctx.send("What is your full name?")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id

    if user_id in user_states:
        state = user_states[user_id]
        
        # Step 1: Get Name
        if state['step'] == 'name':
            state['name'] = message.content.strip()
            state['step'] = 'events'
            await message.channel.send("Which events did you attend? Please separated by comma (e.g. 0x01, 0x02)")
        
        # Step 2: Get Events
        elif state['step'] == 'events':
            events = [e.strip() for e in message.content.split(',')]
            num_events = len(events)
            credits = num_events * 3
            state['events'] = events
            state['credits'] = credits

            # Here you would generate the certificate file
            await message.channel.send(
                f"Thank you, {state['name']}! Generating your certificate for {num_events} events ({credits} CPE credits)..."
            )

            # TODO: generate and send certificate (PDF or image)
            await message.channel.send("Here is your certificate! (Feature not implemented yet)")

            # Clear state
            del user_states[user_id]

    await bot.process_commands(message)

bot.run(TOKEN)