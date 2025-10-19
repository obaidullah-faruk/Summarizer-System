from sqlmodel import SQLModel, Field
from datetime import date, datetime
from typing import Optional
import uuid


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    user_name: Optional[str] = Field(default=None, unique=True, nullable=True)
    name: Optional[str]
    email: str = Field(unique=True)
    password_hash: Optional[str] = None
    created_at: date = Field(default=datetime.now())
