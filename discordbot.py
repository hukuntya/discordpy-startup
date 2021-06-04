import discord 
import os
import traceback

bot = discord.Client() 
token = os.environ['DISCORD_BOT_TOKEN']

@client.event
async def on_message(message):
    if message.author != client.user:
        msg = message.content
        await message.channel.send(msg)

bot.run(token)
