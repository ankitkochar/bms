# Intelligent Book Management System (BMS)

An intelligent and secure Book Management System built with **FastAPI**, **PostgreSQL**, and **LLMs (LLaMA 3 / Mistral via Ollama)**. The system allows users to manage books, write reviews, generate AI-powered summaries, and receive smart recommendations. JWT-based authentication ensures secure access to protected routes.

---

## Features

- User registration & login with JWT authentication
- CRUD operations for books
- Add, view, update, and delete reviews
- Generate summaries using LLaMA 3 or Mistral via Ollama
- Book recommendations powered by LLM
- Search and filter capabilities
- Auto-generated API docs with Swagger and Redoc
- Unit testing with httpx and Python

---

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (`python-jose`, `passlib`)
- **AI Integration**: Ollama (LLaMA 3 / Mistral)
- **Testing**: httpx, asyncio
- **Environment Management**: python-dotenv

---

## Project Structure

```
bms/
├── .env
├── main.py                # Entry point for FastAPI application
├── readme.md              # Project documentation
├── requirements.txt       # Python dependencies
├── app/
│   ├── auth.py            # JWT-based authentication logic
│   ├── crud.py            # CRUD operations for books, reviews, and users
│   ├── database.py        # Database engine and session setup
│   ├── llama.py           # LLaMA model integration logic
│   ├── models.py          # SQLAlchemy models for DB schema
│   ├── schemas.py         # Pydantic models for data validation
│   └── routes/
│       ├── auth_routes.py  # Routes related to user registration and login
│       ├── books.py        # Routes for book CRUD operations
│       └── reviews.py      # Routes for book reviews
├── test/
│   ├── test_apis.py       # Pytest-based API tests
│   └── __init__.py

```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ankitkochar/bms.git
cd bms
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Activate the environment:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/bookdb
SECRET_KEY=your-secret-key
MODEL_NAME=mistral or llama3
```

### 5. Start PostgreSQL

Ensure PostgreSQL is running and create the database (e.g., `bookdb`).

---

## Running the App

```bash
uvicorn app.main:app --reload
```

API available at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## LLM Summary & Recommendation

Make sure [Ollama](https://ollama.com) is installed and running:

```bash
ollama run mistral
# or
ollama run llama3
```

The app integrates with `http://localhost:11434` by default for summary/recommendation generation.

---

## Running Tests

```bash
python test\test_apis.py
```

---

# Here are the information about all the endpoints

## Authentication

### Register

**POST** `/register`

```json
{
  "username": "ankit1",
  "password": "ankit123"
}
```

### Login

**POST** `/token`

Form-data:
- `username`
- `password`

Response:
```json
{
  "access_token": "your.jwt.token",
  "token_type": "bearer"
}
```

---

## Book Endpoints (Require Bearer Token)

### Create Book

**POST** `/books`

```json
{
  "title": "Book Title",
  "author": "Author Name",
  "genre": "Fiction",
  "summary": "Optional book description"
}
```

### Get All Books

**GET** `/books`

### Get Book by ID

**GET** `/books/{book_id}`

### Update Book

**PUT** `/books/{book_id}`

```json
{
  "title": "Updated Title",
  "author": "Updated Author",
  "genre": "Updated Genre",
  "summary": "Updated Summary"
}
```

### Delete Book

**DELETE** `/books/{book_id}`

---

## Reviews

### Add Review

**POST** `/books/{book_id}/reviews`

```json
{
  "reviewer": "Alice",
  "comment": "Amazing book",
  "rating": 4.5
}
```

### Get All Reviews

**GET** `/books/{book_id}/reviews`

---

## Summary & Recommendation

### Get Summary & Average Rating

**GET** `/books/{book_id}/summary`

### Generate Summary (LLM)

**POST** `/generate-summary`

```json
{
  "content": "Long content of the book"
}
```

### Get Recommendations

**GET** `/recommendations`

Query parameters (optional):
- `preferred_genre`

---

## Root Endpoint

**GET** `/`

Returns:
```json
{ "message": "Book Manager API" }
```

## Author

Developed by Ankit Kochar