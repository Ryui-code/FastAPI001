from fstsite.database.schema import ProductOutSchema, ProductInputSchema
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

@products_router.post('/', response_model=ProductOutSchema, summary='Create product.', tags=['Products'])
async def create_product(product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.model_dump())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@products_router.get('/', response_model=List[ProductOutSchema], summary='Get all products.', tags=['Products'])
async def products_list(db: Session = Depends(get_db)):
    products_db = db.query(Product).all()
    if not products_db:
        raise HTTPException(status_code=404, detail='No products.')
    return products_db

@products_router.get('/{product_id}/', response_model=ProductOutSchema, summary='Get product by id.', tags=['Products'])
async def product_detail(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id==product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product not founded by this id.')
    return product_db

@products_router.put('/{product_id/}', response_model=dict, summary='Change product.', tags=['Products'])
async def product_update(product_id: int, product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db1 = db.query(Product).filter(Product.id==product_id).first()
    if not product_db1:
        raise HTTPException(status_code=404, detail='Product not founded by this id.')
    for key, value in product.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product_db1)
    return {'detail': 'Product has been changed.'}

@products_router.delete('/{product_id}/', response_model=dict, summary='Delete product.', tags=['Products'])
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    product_db2 = db.query(Product).filter(Product.id==product_id).first()
    if not product_db2:
        raise HTTPException(status_code=404, detail='Product not founded by this id.')
    db.delete(product_db2)
    db.commit()
    return {'detail': 'Product has been deleted.'}