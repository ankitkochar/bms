from fastapi import FastAPI
from app.routes import books, reviews
from app.database import engine
from app import models
from app.auth import register_user, RegisterUser
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth import register_user, RegisterUser
from app.routes import auth_routes  # or wherever your auth routes are
import logging
import os

os.environ["PYTHONIOENCODING"] = "utf-8"
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

app = FastAPI()

app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(auth_routes.router)

@app.get("/")
async def root():
    return {"message": "Book Manager API"}


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/register")
async def register(user: RegisterUser, db: AsyncSession = Depends(get_db)):
    return await register_user(user, db)