from fstsite.database.schema import ReviewSchema
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

@reviews_router.post('/', summary='Create review.', tags=['Reviews'])
async def create_review(review: ReviewSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.model_dump())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return db

@reviews_router.get('/', response_model=List[ReviewSchema], summary='Get all reviews.', tags=['Reviews'])
async def reviews_list(db: Session = Depends(get_db)):
    reviews_db = db.query(Review).all()
    if not reviews_db:
        raise HTTPException(status_code=404, detail='No reviews.')
    return reviews_db

@reviews_router.get('/', summary='Get review by id.', tags=['Reviews'])
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id==review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail='Review not founded by this id.')
    return review_db