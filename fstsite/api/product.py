from fstsite.database.schema import ProductSchema
from fstsite.database.models import Product
from typing import List
from sqlalchemy.orm import Session
from fstsite.database.db import SessionLocal
from fastapi import Depends, HTTPException, APIRouter

products_router = APIRouter(prefix='/products')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@products_router.post('/', summary='Create product.', tags=['Products'])
async def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.model_dump())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return db

@products_router.get('/', response_model=List[ProductSchema], summary='Get all products.', tags=['Products'])
async def products_list(db: Session = Depends(get_db)):
    products_db = db.query(Product).all()
    if not products_db:
        raise HTTPException(status_code=404, detail='No products.')
    return products_db

@products_router.get('/{product_id}/', summary='Get product by id.', tags=['Products'])
async def product_detail(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id==product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product not founded by this id.')
    return product_db