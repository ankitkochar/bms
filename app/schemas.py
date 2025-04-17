from pydantic import BaseModel
from typing import Optional, List

class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

class BookUpdate(BookBase):
    summary: Optional[str] = None

class BookResponse(BookBase):
    id: int
    summary: Optional[str]
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: int

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    summary: str
    average_rating: Optional[float] = None

class RecommendationRequest(BaseModel):
    preferred_genre: Optional[str] = None
    min_rating: Optional[float] = None

class BookSummaryRequest(BaseModel):
    content: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True