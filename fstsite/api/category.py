from fstsite.database.schema import CategoryOutSchema, CategoryInputSchema
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

@categories_router.post('/', response_model=CategoryOutSchema, summary='Create category.', tags=['Categories'])
async def create_category(category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_db = Category(**category.model_dump())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db

@categories_router.get('/', response_model=List[CategoryOutSchema], summary='Get all categories.', tags=['Categories'])
async def categories_list(db: Session = Depends(get_db)):
    categories_db = db.query(Category).all()
    if not categories_db:
        raise HTTPException(status_code=404, detail='No categories.')
    return categories_db

@categories_router.get('/{category_id}/', response_model=CategoryOutSchema, summary='Get category by id.', tags=['Categories'])
async def category_detail(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id==category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Category not founded by this id.')
    return category_db

@categories_router.put('/{category_id/}', response_model=dict, summary='Change category', tags=['Categories'])
async def category_update(category_id: int, category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_db1 = db.query(Category).filter(Category.id==category_id).first()
    if not category_db1:
        raise HTTPException(status_code=404, detail='Category not founded by this id.')
    for key, value in category.dict().items():
        setattr(category_db1, key, value)
    db.commit()
    db.refresh(category_db1)
    return {'detail': 'Category has been changed. '}

@categories_router.delete('/{category_id}/', response_model=dict, summary='Delete category.', tags=['Categories'])
async def category_delete(category_id: int, db: Session = Depends(get_db)):
    category_db2 = db.query(Category).filter(Category.id==category_id).first()
    if not category_db2:
        raise HTTPException(status_code=404, detail='Category not founded by this id.')
    db.delete(category_db2)
    db.commit()
    return {'detail': 'Category has been deleted.'}