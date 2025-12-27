from fstsite.database.models import CustomUser
from fstsite.database.db import SessionLocal
from fastapi import APIRouter, HTTPException, Depends
from fstsite.database.schema import CustomUserOutSchema, CustomUserInputSchema
from sqlalchemy.orm import Session
from typing import List

users_router = APIRouter(prefix='/users')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post('/', response_model=CustomUserOutSchema, summary='Create user', tags=['Users'])
async def create_user(user: CustomUserInputSchema, db: Session = Depends(get_db)):
    user_db = CustomUser(**user.model_dump())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@users_router.get('/', response_model=List[CustomUserOutSchema], summary='Get all users', tags=['Users'])
async def users_list(db: Session = Depends(get_db)):
    users_db = db.query(CustomUser).all()
    if not users_db:
        raise HTTPException(detail='Такого пользователя нет.', status_code=404)
    return users_db

@users_router.get('/{user_id}/', response_model=CustomUserOutSchema, summary='Get user by id', tags=['Users'])
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(CustomUser).filter(CustomUser.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Такого пользователя нет.', status_code=404)
    return user_db