from pydantic import BaseModel, EmailStr, Field


class AuthRequest(BaseModel):
    email: EmailStr
    password:str = Field(min_length=5, max_length=128)


class RegistrationResponse(BaseModel):
    message: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    message: str
