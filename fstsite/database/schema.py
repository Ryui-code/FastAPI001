from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from datetime import date

class StatusChoices(str, Enum):
    active = 'active'
    inactive = 'inactive'

class CustomUserSchema(BaseModel):
    id: int
    username: str | int = Field(min_length=3, max_length=30)
    password: int | str = Field(min_length=6, max_length=30)
    email: EmailStr
    age: Optional[int] = Field(ge=18, le=100)
    phone_number: Optional[str]
    status: StatusChoices = StatusChoices.inactive
    data_registered: date