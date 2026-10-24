import datetime as dt
import logging
import os

import discord
import dotenv
from discord.ext import commands

from db.connection import client_connect
from services.newsapi import NewsAPI

dotenv.load_dotenv()

everything_url = os.getenv("fetchEverythingUrl")
top_headlines_url = os.getenv("fetchTopHeadlinesUrl")
sources_url = os.getenv("fetchSourcesUrl")
api_key = os.getenv("api_key")

NewsAPI = NewsAPI(api_key=api_key, EverythingUrl=everything_url, topHeadlinesUrl=top_headlines_url, sourcesUrl=sources_url)

botToken = os.getenv("discordBotToken")


intents = discord.Intents.default()


class Client(commands.Bot):
    async def setup_hook(self):
        synced = await self.tree.sync()
        print(f"synced {len(synced)} global commands")

    def save_guild(self, guild):
        try:
            client = client_connect()
            db = client[os.getenv("DB_NAME", "userData")]
            collection = db[os.getenv("GUILD_COLLECTION", "guilds")]
            payload = {
                "guild_id": str(guild.id),
                "guild_name": guild.name,
                "owner_id": str(guild.owner_id),
                "member_count": guild.member_count,
                "is_large": guild.large,
                "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
            collection.update_one({"guild_id": str(guild.id)}, {"$set": payload}, upsert=True)
            return payload
        except Exception as exc:
            print(f"Failed to save guild {guild.id}: {exc}")
            return None

    async def on_ready(self):
        print(f"Logged on as {self.user}")

        for guild in self.guilds:
            self.save_guild(guild)

    async def on_guild_join(self, guild):
        self.save_guild(guild)

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send("you reacted")

    @property
    def user(self):
        return super().user


logFile = logging.FileHandler(filename="solt.log", encoding="UTF-8", mode="w")

client = Client(
    command_prefix="#",
    intents=intents,
    member_cache_flags=discord.MemberCacheFlags.from_intents(intents),
    status="dnd",
)

@client.tree.command(name="get", description="Get recent news for selected topics")
async def getNews(interaction: discord.Interaction, topics: str):
    topics = topics.split(",") if topics else []
    print(topics)
    print((dt.date.today() - dt.timedelta(days=1)), (dt.date.today()))
    from_param = (dt.date.today() - dt.timedelta(days=2))
    to_param = (dt.date.today())
    response = await NewsAPI.get_news(interests=topics, from_param=from_param, to_param=to_param)
    print(response)
    if response is None:
        await interaction.response.send_message("The news box is empty")
        return
    resp = response["news_f"]["articles"]
    if not resp:
        raise Exception("There is no news available")
    message = response["news_f"]["articles"][0]
    title = response["news_f"]["articles"][0]["title"]
    desc = response["news_f"]["articles"][0]["description"]
    url = response["news_f"]["articles"][0]["url"]
    source = response["news_f"]["articles"][0]["source"]["name"]
    img = response["news_f"]["articles"][0]["urlToImage"]

    await interaction.response.send_message(
        f"title: {title} \n desc: {desc} \n url: {url} \n source: {source} \n image: {img}"
    )
    return


client.run(botToken)  # , log_handler=logFile