from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from .models import Book, Review
from . import models, schemas
from app.models import User
from app.schemas import UserCreate
from fastapi import HTTPException

async def create_book(db, book: schemas.BookCreate):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

async def get_books(db: AsyncSession):
    result = await db.execute(select(Book))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int):
    return await db.get(Book, book_id)

async def update_book(db: AsyncSession, book_id: int, book_data):
    book = await get_book(db, book_id)
    for key, value in book_data.dict(exclude_unset=True).items():
        setattr(book, key, value)
    await db.commit()
    return book

async def delete_book(db: AsyncSession, book_id: int):
    book = await get_book(db, book_id)
    await db.delete(book)
    await db.commit()

async def add_review(db: AsyncSession, book_id: int, review_data):
    review = Review(**review_data.dict(), book_id=book_id)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

async def get_reviews(db: AsyncSession, book_id: int):
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    return result.scalars().all()

async def get_avg_rating(db: AsyncSession, book_id: int):
    result = await db.execute(select(func.avg(Review.rating)).where(Review.book_id == book_id))
    return result.scalar()

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: UserCreate):
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(username=user.username, password=user.password)  # 🔐 In real apps, hash passwords!
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user