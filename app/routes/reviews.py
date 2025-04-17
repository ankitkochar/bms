from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas
from ..database import get_db
from typing import List

router = APIRouter()

@router.post("/books/{book_id}/reviews", response_model=schemas.ReviewResponse)
async def add_review(book_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db)):
    return await crud.add_review(db, book_id, review)

@router.get("/books/{book_id}/reviews", response_model=List[schemas.ReviewResponse])
async def get_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_reviews(db, book_id)