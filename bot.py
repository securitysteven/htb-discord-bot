import discord
import os
from discord.ext import commands
from generate_certificate import generate_certificate

TOKEN = os.environ['DISCORD_BOT_TOKEN']

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

user_states = {}

@bot.command(name='cpe', description='Request CPE certificate')
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

        if state['step'] == 'name':
            state['name'] = message.content.strip()
            state['step'] = 'events'
            await message.channel.send("Which events did you attend? Please separate by comma (e.g. 0x01, 0x02)")

        elif state['step'] == 'events':
            events = [e.strip() for e in message.content.split(',')]
            num_events = len(events)
            credits = num_events * 3
            state['events'] = events
            state['credits'] = credits

            await message.channel.send(
                f"Thank you, {state['name']}! Generating your certificate for {num_events} events ({credits} CPE credits)..."
            )

            # Generate PDF
            pdf_buffer = generate_certificate(state['name'], state['events'], state['credits'])

            # Send PDF
            file = discord.File(fp=pdf_buffer, filename="certificate.pdf")
            await message.channel.send("Here is your certificate!", file=file)

            # Clear state
            del user_states[user_id]

    await bot.process_commands(message)

bot.run(TOKEN)