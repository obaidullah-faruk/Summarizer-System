from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.core.config import get_settings
from app.models.user import User
from app.services.auth import get_user_infos_from_google_token_url

router = APIRouter()
settings = get_settings()


@router.get('/google/login')
async def google_login():
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline")


@router.get('/google-callback')
async def google_auth_callback(code: str):
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    result = await get_user_infos_from_google_token_url(code)

    if not result['status']:
        raise HTTPException(status_code=400, detail="Couldn't get user info")

    return result['user_infos']
