import discord 
import os
import traceback

bot = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

bot.run(token)
