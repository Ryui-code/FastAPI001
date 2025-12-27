from fstsite.database.schema import CategorySchema
from fstsite.database.models import Category
from fastapi import HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from fstsite.database.db import SessionLocal

categories_router = APIRouter(prefix='/categories')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@categories_router.post('/', summary='Create category.', tags=['Categories'])
async def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    category_db = Category(**category.model_dump())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db

@categories_router.get('/', response_model=List[CategorySchema], summary='Get all categories.', tags=['Categories'])
async def categories_list(db: Session = Depends(get_db)):
    categories_db = db.query(Category).all()
    if not categories_db:
        raise HTTPException(status_code=404, detail='No categories.')
    return categories_db

@categories_router.get('/{category_id}/', response_model=CategorySchema, summary='Get category by id.', tags=['Categories'])
async def category_detail(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id==category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Category not founded by this id.')
    return category_db