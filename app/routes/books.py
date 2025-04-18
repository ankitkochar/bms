from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, llama
from ..database import get_db
from typing import List
from app.auth import get_current_user
from sqlalchemy.future import select
from app.models import Book, Review

router = APIRouter()

@router.post("/books", response_model=schemas.BookResponse)
async def create(book: schemas.BookCreate, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await crud.create_book(db, book)

@router.get("/books", response_model=List[schemas.BookResponse])
async def read_all(db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await crud.get_books(db)

@router.get("/books/{book_id}", response_model=schemas.BookResponse)
async def read(book_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    book = await crud.get_book(db, book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return book

@router.put("/books/{book_id}", response_model=schemas.BookResponse)
async def update(book_id: int, book_data: schemas.BookUpdate, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await crud.update_book(db, book_id, book_data)

@router.delete("/books/{book_id}")
async def delete(book_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await crud.delete_book(db, book_id)
    return {"detail": "Deleted"}

@router.get("/recommendations", response_model=List[schemas.BookResponse])
async def recommendations(preferences: schemas.RecommendationRequest = Depends(), db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    books = await crud.get_books(db)
    return [b for b in books if (not preferences.preferred_genre or b.genre == preferences.preferred_genre)]


@router.post("/generate-summary")
async def generate_summary_endpoint(request: schemas.BookSummaryRequest, current_user: str = Depends(get_current_user)):
    return await llama.generate_summary(request.content)

@router.get("/books/{id}/summary")
async def get_book_summary_and_rating(id: int, db: AsyncSession = Depends(get_db)):
    # Fetch the book
    result = await db.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Fetch reviews and calculate average rating
    reviews_result = await db.execute(select(Review).where(Review.book_id == id))
    reviews = reviews_result.scalars().all()
    average_rating = round(sum([r.rating for r in reviews]) / len(reviews), 2) if reviews else None

    # Generate a summary
    summary_response = await llama.generate_summary(book.summary)

    return {
        "title": book.title,
        "author": book.author,
        "summary": summary_response,
        "average_rating": average_rating
    }
