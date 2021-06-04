import discord
import os

client = discord.Client()

def out(mess):
    out = ['すぐ消', 'すぐけす', 'すぐけし', '後で消', 'あとで消', 'あとでけす', 'あとでけし']
    flag = False
    
    for s in out:
        if mess.content.count(s) > 0:
            flag = True
            
    return flag
    

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.attachments:
        for attachment in message.attachments:
            if out(message):
                await message.channel.send(file=attachment.url)

client.run(os.environ['DISCORD_BOT_TOKEN'])
