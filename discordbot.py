import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.find('すぐ消') > 0 OR message.content.find('すぐけす') > 0 OR message.content.find('すぐけし') > 0:
        await message.channel.send('言ったな！')

client.run(os.environ['DISCORD_BOT_TOKEN'])
