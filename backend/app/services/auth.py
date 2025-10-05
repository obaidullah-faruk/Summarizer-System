import httpx
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


async def get_user_infos_from_google_token_url(code: str):
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    user_info_url = "https://oauth2.googleapis.com/token"

    async with httpx.AsyncClient() as client:
        resp = await client.post(user_info_url, data=data)
        json_resp = resp.json()
        access_token = json_resp.get("access_token")

    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url=userinfo_url, headers=headers)
        user_info = response.json()

    logger.info(f"User info: {user_info}")
    return {
        "status": bool(user_info),
        "user_infos": user_info
    }
