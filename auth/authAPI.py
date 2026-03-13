from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/google/")
async def google_auth():
    return f'google auth'

@router.get("/discord/")
async def discord_auth():
    return f'discord auth'
