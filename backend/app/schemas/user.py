from pydantic import BaseModel, EmailStr, Field


class RegistrationRequest(BaseModel):
    email: EmailStr
    password:str = Field(min_length=5, max_length=128)


class RegistrationResponse(BaseModel):
    message: str