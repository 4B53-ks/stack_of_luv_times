import os

import dotenv
from fastapi import APIRouter, HTTPException
from jose import JWTError

from auth.discordAuth import DiscordAuth

# from db import connection.client

dotenv.load_dotenv()

discord_auth = DiscordAuth(
    discordAuthURL=os.getenv("discordOAuthURI"),
    discordClientID=os.getenv("discordClientID"),
    discordClientSecret=os.getenv("discordClientSecret"),
    redirectURI=os.getenv("localRedirectURI"),
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/redirect_auth")
def redirect_auth():
    return {"message": "Redirected back from Discord"}


@router.get("/discord")
def discord_login():
    try:
        auth_url = discord_auth.get_auth_url()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"auth_url": auth_url}


@router.get("/discord/callback")
def discord_callback(code: str | None = None, error: str | None = None, state: str | None = None):
    if error:
        raise HTTPException(status_code=400, detail=f"Discord OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code is required.")

    try:
        token_data = discord_auth.exchange_code_for_token(code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"message": "Discord authentication successful", "token_data": token_data}


@router.post("/discordToken")
def exchange_code_for_token(code: str):
    if not code or not code.strip():
        raise HTTPException(status_code=400, detail="Authorization code is required.")

    try:
        token_data = discord_auth.exchange_code_for_token(code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"token_data": token_data}


@router.get("/discordUserInfo")
def get_discord_user_info(access_token: str = None):
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token is required.")

    try:
        user_info = discord_auth.get_user_info(access_token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return {"user_info": user_info}


@router.post("/refresh_token")
def get_refresh_token(refreshToken: str):
    if not refreshToken:
        raise HTTPException(status_code=400, detail="Refresh token is required.")

    try:
        token_data = discord_auth.refresh_token(refreshToken)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"token_data": token_data}


@router.post("/validate-token")
def validate_token(token: str):
    if not token or not token.strip():
        raise HTTPException(status_code=400, detail="JWT token is required.")

    try:
        payload = discord_auth.verify_jwt(token)
    except (ValueError, JWTError) as exc:
        raise HTTPException(status_code=401, detail="JWT token is invalid or expired.") from exc
    return {"valid": True, "token": payload}
