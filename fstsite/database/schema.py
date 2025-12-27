from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from datetime import date

class StatusChoices(str, Enum):
    active = 'active'
    inactive = 'inactive'

class CustomUserOutSchema(BaseModel):
    id: int
    username: str | int = Field(min_length=3, max_length=30)
    password: int | str = Field(min_length=6, max_length=30)
    email: EmailStr
    age: Optional[int] = Field(ge=18, le=100)
    phone_number: Optional[str]
    status: StatusChoices = StatusChoices.inactive
    data_registered: date

class CustomUserInputSchema(BaseModel):
    username: str | int = Field(min_length=3, max_length=30)
    password: int | str = Field(min_length=6, max_length=30)
    email: EmailStr
    age: Optional[int] = Field(ge=18, le=100)
    phone_number: Optional[str]
    status: StatusChoices = StatusChoices.inactive

class CategorySchema(BaseModel):
    id: int
    category_image: str
    category_name: str = Field(min_length=3, max_length=30)

class ProductSchema(BaseModel):
    id: int
    category_id: int
    product_name: str = Field(min_length=3, max_length=30)
    product_image: str
    price: int = Field(ge=1)
    article_number: int
    description: str
    product_video: str
    created_date: date

class ReviewSchema(BaseModel):
    id: int
    user_id: int
    product_id: int
    stars: int = Field(le=5)
    created_date: date