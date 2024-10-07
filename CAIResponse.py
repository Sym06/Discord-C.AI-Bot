import asyncio
from characterai import PyAsyncCAI

class CAIResponse():
    def __init__(self):
        self.accountID = '023ab32bbb1bd142ebd420b33c9f8cb4a8846062'
        self.characterID = '0-Pq4GLx7Mi8JaZG5V0l_3NxyPCzjJue_hlDZIP3gpo'
        self.chat, self.caiClient, self.tgt = None, None, None

    async def startup(self):
        self.caiClient = PyAsyncCAI(self.accountID)
        #await self.caiClient.start()

        self.chat = await self.caiClient.chat.new_chat(self.characterID)

        participants = self.chat['participants']

        if not participants[0]['is_human']:
            self.tgt = participants[0]['user']['username']
        else:
            self.tgt = participants[1]['user']['username']

    async def respond(self, message):
        data = await self.caiClient.chat.send_message(
            self.chat['external_id'], self.tgt, message
        )

        text = data['replies'][0]['text']

        return text