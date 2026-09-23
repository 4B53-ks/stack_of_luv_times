import discord
import dotenv
import os
import datetime as dt
import logging
from discord.ext import commands
from discord import app_commands
from services.newsapi import NewsAPI

dotenv.load_dotenv()
everything_url = os.getenv("fetchEverythingUrl")
top_headlines_url = os.getenv("fetchTopHeadlinesUrl")
sources_url = os.getenv("fetchSourcesUrl")
api_key = os.getenv("api_key")

NewsAPI = NewsAPI(api_key=api_key, EverythingUrl=everything_url, topHeadlinesUrl=top_headlines_url, sourcesUrl=sources_url)

botToken=os.getenv('discordBotToken')


intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        
        try:
            guild = discord.Object(id=1222787258634207262)
            synced = await self.tree.sync(guild=guild)
            print(f'synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'error {e}')
            
        
    async def on_message(self, message) -> dict:
        if message.author == self.user:
            return
        
        print(f"message from {message.author}:{message.content}")
        return {"Message":message,"code":200}
    
    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('you reacted')
    
    @property
    def user(self):
        return super().user
    
logFile = logging.FileHandler(filename="solt.log",encoding="UTF-8", mode="w")

client = Client(command_prefix="#", intents=intents,member_cache_flags=discord.MemberCacheFlags.from_intents(intents),status='dnd')

GUILD_ID = discord.Object(id=1222787258634207262)

@client.tree.command(name="get",description="news phekh", guild=GUILD_ID)
async def getNews(interaction: discord.Interaction, topics: str):
    topics = topics.split(",") if topics else []
    print(topics)
    print((dt.date.today() - dt.timedelta(days = 1)), (dt.date.today()))
    from_param=(dt.date.today() - dt.timedelta(days = 2))
    to_param=(dt.date.today())
    response = await NewsAPI.get_news(interests=topics, from_param=from_param, to_param=to_param)
    print(response)
    if None == response:
        await interaction.response.send_message(f'The news box is empty')
        return
    resp = response['news_f']['articles']
    if False==bool(resp):
        raise Exception("There is no news available")
    message = response['news_f']['articles'][0]
    title = response['news_f']['articles'][0]['title']
    desc = response['news_f']['articles'][0]['description']
    url = response['news_f']['articles'][0]['url']
    source = response['news_f']['articles'][0]['source']['name']
    img = response['news_f']['articles'][0]['urlToImage']
    
    embed = discord.Embed(title="Hello world",)
    
    await interaction.response.send_message(f'title: {title} \n desc: {desc} \n url: {url} \n source: {source} \n image: {img}')
    return

client.run(botToken)#, log_handler=logFile