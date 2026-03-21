from fastapi import APIRouter
from auth.discordAuth import DiscordAuth
import dotenv
import os

dotenv.load_dotenv()
discord_auth = DiscordAuth(
    discordAuthURL=os.getenv("discordOAuthURI"),
    discordClientID=os.getenv("discordClientID"),
    discordClientSecret=os.getenv("discordClientSecret"),
    redirectURI=os.getenv("localRedirectURI")
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/redirect_auth")
def redirect_auth():
    # to read the incoming params
    return {"message": "Redirected back from Discord"}

@router.get("/discord")
def discord_login():
    auth_url = discord_auth.get_auth_url()
    return {"auth_url": auth_url}

@router.get("/discordToken")
def exchange_code_for_token(code: str=None):
    token_data = discord_auth.exchange_code_for_token(code)
    return {"token_data": token_data}