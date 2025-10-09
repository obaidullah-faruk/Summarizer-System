from pwdlib import PasswordHash
import jwt
import datetime
from uuid import UUID
from app.core.config import get_settings

password_hash = PasswordHash.recommended()
settings = get_settings()

def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    is_valid = password_hash.verify(password, hashed_password)
    return is_valid


def create_access_token(user_id: UUID):
    access_payload = {
        'user_id': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=settings.JWT_ACCESS_TOKEN_VALIDITY),  # Expires in 30 minutes
        'iat': datetime.datetime.utcnow(),
        'type': 'access'
    }
    access_token = jwt.encode(access_payload, settings.JWT_SECRET , algorithm='HS256')
    return access_token


def create_refresh_token(user_id: UUID):
    refresh_payload = {
        'user_id': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=settings.JWT_REFRESH_TOKEN_VALIDITY),  # Expires in 30 minutes
        'iat': datetime.datetime.utcnow(),
        'type': 'refresh'
    }
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET , algorithm='HS256')
    return refresh_token