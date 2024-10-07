import discord
import re
import time
import asyncio, nest_asyncio
from CAIResponse import CAIResponse
from colorama import Fore

nest_asyncio.apply()

responseClass = CAIResponse()

messageList = []
isResponding = False

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    try:
        await responseClass.startup()
        print("Character AI is on!")
    except Exception as error:
        print(f'{Fore.RED}ERROR {Fore.RESET} {str(error)}')

    print('Bot is on and ready!\n----------------------')

@client.event
async def on_message(msg):
    if msg.author == client.user: return

    if msg.mentions and client.user in msg.mentions:
        messageList.append(msg)
        global isResponding
        if isResponding == True: return
        first = time.perf_counter()
        while messageList:
            for message in messageList:
                async with msg.channel.typing():
                    isResponding = True
                    fullMessage = message.content.replace(client.user.mention + " ", '', 1)
                    response = asyncio.run(responseClass.respond(fullMessage))

                    correctedResponse = re.sub("Sym", message.author.mention, response, flags=re.IGNORECASE)
                    await message.reply(correctedResponse)

                    messageList.remove(message)
        
        second = time.perf_counter()
        print(f'{float(second) - float(first)} seconds')
        isResponding = False


client.run('(token)')