from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from app.core.config import get_settings
from app.services.auth import get_user_infos_from_google_token_url
from app.schemas.user import AuthRequest, RegistrationResponse, LoginResponse
from app.database.deps import SessionDep
from app.crud.user import check_user_exists, create_user, get_password
from app.core.logging import logger
from app.utils.auth import get_password_hash, verify_password, create_access_token, create_refresh_token


router = APIRouter()
settings = get_settings()


@router.post('/register', response_model = RegistrationResponse)
def register(user_data: AuthRequest, session: SessionDep):
    email = user_data.email.strip().lower()
    user_exits = check_user_exists(email, session)
    if user_exits:
         logger.error(f'User already exists for this email: {email}')
         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    password_hash=get_password_hash(user_data.password)
    user = create_user(email, password_hash, session)
    logger.info(f"New user created with email {email}. ID: {user.id}")
    return RegistrationResponse(message= "Registration successful")


@router.post('/login', response_model = LoginResponse)
def login(user_cred: AuthRequest, session: SessionDep):
    email = user_cred.email.strip().lower()
    password = user_cred.password.strip()

    user_pass = get_password(email, session)
    if user_pass is None:
        raise HTTPException(status_code=404, detail="Account not available")
    
    verify = verify_password(password, user_pass.password_hash)
    if verify:
        logger.info(f"Password matched for login. Email: {email}")
        access_token = create_access_token(user_pass.id)
        logger.info("Access token generated")
        refresh_token = create_refresh_token(user_pass.id)
        logger.info("Refresh token generated")
        return LoginResponse(access_token=access_token, refresh_token=refresh_token, message= "Login successful")
    else:
        logger.error(f"Login Unsuccessful. Email: {email}")
        raise HTTPException(status_code=401, detail="Password not matched")


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
