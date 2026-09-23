import discord
import dotenv
import os

dotenv.load_dotenv()

botToken=os.getenv('discordBotToken')


intents = discord.Intents.default()
intents.message_content = True

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        
    async def on_message(message:str=None) -> dict:
        return {"Message":message,"code":200}
    
client = Client(intents=intents)
client.run(botToken)