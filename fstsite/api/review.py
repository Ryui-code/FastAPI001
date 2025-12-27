from fstsite.database.schema import ReviewOutSchema, ReviewInputSchema
from fstsite.database.models import Review
from typing import List
from sqlalchemy.orm import Session
from fstsite.database.db import SessionLocal
from fastapi import Depends, HTTPException, APIRouter

reviews_router = APIRouter(prefix='/reviews')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@reviews_router.post('/', response_model=ReviewOutSchema, summary='Create review.', tags=['Reviews'])
async def create_review(review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.model_dump())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@reviews_router.get('/', response_model=List[ReviewOutSchema], summary='Get all reviews.', tags=['Reviews'])
async def reviews_list(db: Session = Depends(get_db)):
    reviews_db = db.query(Review).all()
    if not reviews_db:
        raise HTTPException(status_code=404, detail='No reviews.')
    return reviews_db

@reviews_router.get('/{review_id/}', response_model=ReviewOutSchema, summary='Get review by id.', tags=['Reviews'])
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id==review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail='Review not founded by this id.')
    return review_db

@reviews_router.put('/{review_id/}', response_model=dict, summary='Change review.', tags=['Reviews'])
async def review_update(review_id: int, review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db1 = db.query(Review).filter(Review.id==review_id).first()
    if not review_db1:
        raise HTTPException(status_code=404, detail='Review not founded by this id.')
    for key, value in review.dict().items():
        setattr(review_db1, key, value)
    db.commit()
    db.refresh(review_db1)
    return {'detail': 'Review has been changed.'}

@reviews_router.delete('/{review_id}/', response_model=dict, summary='Delete review.', tags=['Reviews'])
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    review_db2 = db.query(Review).filter(Review.id==review_id).first()
    if not review_db2:
        raise HTTPException(status_code=404, detail='Review not founded by this id.')
    db.delete(review_db2)
    db.commit()
    return {'detail': 'Review has been deleted.'}