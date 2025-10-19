from pwdlib import PasswordHash
import jwt
import datetime
from uuid import UUID
from app.core.config import get_settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from app.crud.user import get_user
from app.database.deps import SessionDep
from app.core.logging import logger

password_hash = PasswordHash.recommended()
bearer_scheme = HTTPBearer()

settings = get_settings()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    is_valid = password_hash.verify(password, hashed_password)
    return is_valid


def create_access_token(user_id: UUID):
    access_payload = {
        'user_id': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=settings.JWT_ACCESS_TOKEN_VALIDITY),
        'iat': datetime.datetime.utcnow(),
        'type': 'access'
    }
    access_token = jwt.encode(access_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return access_token


def create_refresh_token(user_id: UUID):
    refresh_payload = {
        'user_id': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=settings.JWT_REFRESH_TOKEN_VALIDITY),
        'iat': datetime.datetime.utcnow(),
        'type': 'refresh'
    }
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return refresh_token


def get_current_user(session: SessionDep, token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(user_id=user_id, session=session)
    if user is None:
        logger.error(f"Token verified Failed. Token: {token}")
        raise credentials_exception
    logger.info(f"Token verified for user ID: {user_id}")
    return user.id
