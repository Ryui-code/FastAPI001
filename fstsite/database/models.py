from typing import Optional, List
from datetime import date
from sqlalchemy import Integer, String, Date, ForeignKey, Text, Enum
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

class StatusChoices(str, PyEnum):
    active = 'active'
    inactive = 'inactive'

class CustomUser(Base):
    __tablename__ = 'custom_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str | int] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(20))
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.inactive)
    data_registered: Mapped[date] = mapped_column(Date, default=date.today)

    user_review: Mapped[List["Review"]] = relationship(back_populates="user", cascade='all, delete-orphan')

class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(30), unique=True)
    category_image: Mapped[str] = mapped_column(String)

    products_category: Mapped[List["Product"]] = relationship("Product", back_populates="category", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    product_name: Mapped[str] = mapped_column(String)
    product_image: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    article_number: Mapped[int] = mapped_column(Integer, unique=True)
    description: Mapped[str] = mapped_column(Text)
    product_video: Mapped[str] = mapped_column(String)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    product_review: Mapped[List["Review"]] = relationship("Review", back_populates="product")
    category: Mapped[Category] = relationship(Category, back_populates='products_category')

class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('custom_user.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    stars: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    user: Mapped[CustomUser] = relationship(CustomUser, back_populates='user_review')
    product: Mapped[Product] = relationship(Product, back_populates='product_review')