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
    
    out = ['すぐ消', 'すぐけす', 'すぐけし', '後で消', 'あとで消', 'あとでけす', 'あとでけし']
    flag = False
    
    for s in out:
        if if message.content.count(s) > 0:
            flag = True
    
    if flag:
        await message.channel.send('言ったな！')
    
    if message.attachments:
        for attachment in message.attachments:
            if attachment.url.endswith(("png", "jpg", "jpeg")):
                await message.channel.send(attachment.url)

client.run(os.environ['DISCORD_BOT_TOKEN'])
