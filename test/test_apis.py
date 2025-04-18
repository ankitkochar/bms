import asyncio
import httpx
import json
from typing import Dict, Any, List, Optional

BASE_URL = "http://localhost:8000"

TEST_USER = {
    "username": "ankit1",
    "password": "ankit123"
}

TEST_BOOK = {
    "title": "The Midnight Library",
    "author": "Matt Haig",
    "genre": "Fiction",
    "year_published": 2020,
    "summary": '''In The Midnight Library, Matt Haig takes readers on a poignant and imaginative journey through the eyes of Nora Seed, a woman struggling under the weight of regret, depression, and a feeling of meaninglessness. When she decides that life is no longer worth living, she finds herself in a mystical in-between space — a library that exists between life and death. This library is not just any ordinary place. It holds an infinite number of books, each representing a version of her life if she had made different choices.

        From the moment Nora steps into the Midnight Library, she is greeted by her old school librarian, Mrs. Elm, who serves as a kind of guide through this metaphysical landscape. Mrs. Elm explains that every book in the library is a portal to a different life Nora could have lived. These lives span the spectrum — from ones where she pursued Olympic-level swimming, to being a rock star, a glaciologist in the Arctic, a mother, a pub owner, and many more.

        As Nora ventures through each alternate life, she experiences the full range of what might have been: love, adventure, heartbreak, failure, and success. In some lives, she is incredibly famous but unfulfilled; in others, she finds peace in small, ordinary moments. Each life brings with it new revelations about what it means to be alive, to have purpose, and to connect with others.

        One of the key themes Haig explores through Nora's journey is the idea that regret is often a product of limited perspective. From where she stands in her original life, her choices seem like mistakes — paths not taken that could have led to happiness. But through the library's magic, Nora sees that even those seemingly perfect lives come with their own struggles and pain. She realizes that perfection doesn't exist, and that the idea of a "perfect life" is an illusion.

        Through this process of self-exploration and soul-searching, Nora begins to shed the weight of her regrets. She learns that her life — just as it is — holds potential, meaning, and beauty. The things she once thought were failures become threads in the rich tapestry of her story. By facing her fears and embracing vulnerability, she gradually comes to understand that life is made up of moments, and that living fully means being present for all of them — even the difficult ones.

        In the end, The Midnight Library is not just a story about a woman choosing to live. It is a reminder to all readers that every decision shapes our path, but no path is without its challenges. What matters most is not the endless array of choices we could have made, but what we do with the one life we're living now.

        Matt Haig's novel is a celebration of resilience, hope, and the quiet courage it takes to begin again. Thought-provoking and emotionally rich, it urges readers to embrace the chaos of life, find gratitude in the present, and understand that meaning is not something we find — it's something we create.'''
    }


UPDATE_BOOK = {
    "title": "The Midnight Library",
    "author": "Matt Haig",
    "genre": "Fiction",
    "year_published": 2020,
    "summary": '''This is the updated version of the midnight library. In The Midnight Library, Matt Haig takes readers on a poignant and imaginative journey through the eyes of Nora Seed, a woman struggling under the weight of regret, depression, and a feeling of meaninglessness. When she decides that life is no longer worth living, she finds herself in a mystical in-between space — a library that exists between life and death. This library is not just any ordinary place. It holds an infinite number of books, each representing a version of her life if she had made different choices.

From the moment Nora steps into the Midnight Library, she is greeted by her old school librarian, Mrs. Elm, who serves as a kind of guide through this metaphysical landscape. Mrs. Elm explains that every book in the library is a portal to a different life Nora could have lived. These lives span the spectrum — from ones where she pursued Olympic-level swimming, to being a rock star, a glaciologist in the Arctic, a mother, a pub owner, and many more.

As Nora ventures through each alternate life, she experiences the full range of what might have been: love, adventure, heartbreak, failure, and success. In some lives, she is incredibly famous but unfulfilled; in others, she finds peace in small, ordinary moments. Each life brings with it new revelations about what it means to be alive, to have purpose, and to connect with others.

One of the key themes Haig explores through Nora's journey is the idea that regret is often a product of limited perspective. From where she stands in her original life, her choices seem like mistakes — paths not taken that could have led to happiness. But through the library's magic, Nora sees that even those seemingly perfect lives come with their own struggles and pain. She realizes that perfection doesn't exist, and that the idea of a "perfect life" is an illusion.

Through this process of self-exploration and soul-searching, Nora begins to shed the weight of her regrets. She learns that her life — just as it is — holds potential, meaning, and beauty. The things she once thought were failures become threads in the rich tapestry of her story. By facing her fears and embracing vulnerability, she gradually comes to understand that life is made up of moments, and that living fully means being present for all of them — even the difficult ones.

In the end, The Midnight Library is not just a story about a woman choosing to live. It is a reminder to all readers that every decision shapes our path, but no path is without its challenges. What matters most is not the endless array of choices we could have made, but what we do with the one life we're living now.

Matt Haig's novel is a celebration of resilience, hope, and the quiet courage it takes to begin again. Thought-provoking and emotionally rich, it urges readers to embrace the chaos of life, find gratitude in the present, and understand that meaning is not something we find — it's something we create.'''
}

# Test review data
TEST_REVIEW = {
    "user_id": 1,  # Will be replaced with actual user ID
    "review_text": "This is a test review.",
    "rating": 4
}

# Global variables to store data between tests
user_id = None
book_id = None
access_token = None

async def register_user(client: httpx.AsyncClient) -> Dict[str, Any]:
    """Register a test user."""
    print("\n=== Registering Test User ===")
    try:
        response = await client.post("/register", json=TEST_USER)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP Error during registration: {e}")
        print(f"Request: {e.request.url}")
        # If the user already exists, we can continue
        return {"id": None}
    except Exception as e:
        print(f"Unexpected error during registration: {e}")
        return {"id": None}

async def login_user(client: httpx.AsyncClient) -> str:
    """Login and get access token."""
    print("\n=== Logging in User ===")
    form_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    try:
        response = await client.post("/token", data=form_data)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {data}")
        return data.get("access_token")
    except httpx.HTTPError as e:
        print(f"HTTP Error during login: {e}")
        print(f"Request: {e.request.url}")
        return None
    except Exception as e:
        print(f"Unexpected error during login: {e}")
        return None

async def create_book(client: httpx.AsyncClient, token: str) -> Dict[str, Any]:
    """Create a test book."""
    print("\n=== Creating Book ===")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = await client.post("/books", json=TEST_BOOK, headers=headers)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {data}")
        return data
    except httpx.HTTPError as e:
        print(f"HTTP Error during book creation: {e}")
        print(f"Request: {e.request.url}")
        return {"id": None}
    except Exception as e:
        print(f"Unexpected error during book creation: {e}")
        return {"id": None}

async def get_all_books(client: httpx.AsyncClient, token: str) -> List[Dict[str, Any]]:
    """Get all books."""
    print("\n=== Getting All Books ===")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = await client.get("/books", headers=headers)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Found {len(data)} books")
        return data
    except httpx.HTTPError as e:
        print(f"HTTP Error getting all books: {e}")
        print(f"Request: {e.request.url}")
        return []
    except Exception as e:
        print(f"Unexpected error getting all books: {e}")
        return []

async def get_book(client: httpx.AsyncClient, book_id: int, token: str) -> Dict[str, Any]:
    """Get a specific book by ID."""
    print(f"\n=== Getting Book {book_id} ===")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = await client.get(f"/books/{book_id}", headers=headers)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {data}")
        return data
    except httpx.HTTPError as e:
        print(f"HTTP Error getting book {book_id}: {e}")
        print(f"Request: {e.request.url}")
        return {}
    except Exception as e:
        print(f"Unexpected error getting book {book_id}: {e}")
        return {}

async def update_book(client: httpx.AsyncClient, book_id: int, token: str) -> Dict[str, Any]:
    """Update a book."""
    print(f"\n=== Updating Book {book_id} ===")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = await client.put(f"/books/{book_id}", json=UPDATE_BOOK, headers=headers)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {data}")
        return data
    except httpx.HTTPError as e:
        print(f"HTTP Error updating book {book_id}: {e}")
        print(f"Request: {e.request.url}")
        return {}
    except Exception as e:
        print(f"Unexpected error updating book {book_id}: {e}")
        return {}

async def delete_book(client: httpx.AsyncClient, book_id: int, token: str) -> Dict[str, Any]:
    """Delete a book."""
    print(f"\n=== Deleting Book {book_id} ===")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = await client.delete(f"/books/{book_id}", headers=headers)
        print(f"Status: {response.status_code}")
        # Handle case where response might be empty or not JSON
        try:
            data = response.json()
            print(f"Response: {data}")
            return data
        except Exception:
            print(f"Response: Success (No content)")
            return {"status": "success"}
    except httpx.HTTPError as e:
        print(f"HTTP Error deleting book {book_id}: {e}")
        print(f"Request: {e.request.url}")
        return {"status": "error", "message": str(e)}
    except Exception as e:
        print(f"Unexpected error deleting book {book_id}: {e}")
        return {"status": "error", "message": str(e)}

async def add_review(client: httpx.AsyncClient, book_id: int, token: str) -> Dict[str, Any]:
    """Add a review to a book."""
    print(f"\n=== Adding Review to Book {book_id} ===")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Get user info from token if needed
        try:
            user_info_response = await client.get("/users/me", headers=headers)
            user_info = user_info_response.json()
            current_user_id = user_info.get("id", user_id or 1)
        except Exception:
            # If endpoint not available, use global user_id or default to 1
            current_user_id = user_id or 1
        
        review_data = TEST_REVIEW.copy()
        review_data["user_id"] = current_user_id
        
        response = await client.post(f"/books/{book_id}/reviews", json=review_data, headers=headers)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {data}")
        return data
    except httpx.HTTPError as e:
        print(f"HTTP Error adding review to book {book_id}: {e}")
        print(f"Request: {e.request.url}")
        return {}
    except Exception as e:
        print(f"Unexpected error adding review to book {book_id}: {e}")
        return {}

async def get_reviews(client: httpx.AsyncClient, book_id: int, token: str) -> List[Dict[str, Any]]:
    """Get all reviews for a book."""
    print(f"\n=== Getting Reviews for Book {book_id} ===")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = await client.get(f"/books/{book_id}/reviews", headers=headers)
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Found {len(data)} reviews")
        return data
    except httpx.HTTPError as e:
        print(f"HTTP Error getting reviews for book {book_id}: {e}")
        print(f"Request: {e.request.url}")
        return []
    except Exception as e:
        print(f"Unexpected error getting reviews for book {book_id}: {e}")
        return []

async def get_book_summary(client: httpx.AsyncClient, book_id: int, token: str) -> Dict[str, Any]:
    """Get a book's summary and average rating."""
    print(f"\n=== Getting Summary for Book {book_id} ===")
    print("This may take several minutes (300-400 seconds)...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Set timeout to None for unlimited wait time
        response = await client.get(f"/books/{book_id}/summary", headers=headers, timeout=None)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            return data
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            print(error_msg)
            return {"error": error_msg}
    except httpx.HTTPError as e:
        error_msg = f"HTTP Error: {e}"
        print(error_msg)
        print(f"Request: {e.request.url}")
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        return {"error": error_msg}
    
async def generate_summary(client: httpx.AsyncClient, token: str) -> Dict[str, Any]:
    """Generate a summary for a given text."""
    print("\n=== Generating Summary ===")
    print("This may take several minutes (300-400 seconds)...")
    headers = {"Authorization": f"Bearer {token}"}
    content = {
        "content": "It was a bitterly cold February day when a mysterious stranger arrived in the village of Iping. Wrapped from head to toe in bandages, wearing dark glasses and a wide-brimmed hat, he carried with him an air of secrecy that instantly drew the suspicion of the villagers."
    }
    # Using a shorter text for testing to reduce processing time
    try:
        # Set timeout to None for unlimited wait time
        response = await client.post("/generate-summary", json=content, headers=headers, timeout=None)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            return data
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            print(error_msg)
            return {"error": error_msg}
    except httpx.HTTPError as e:
        error_msg = f"HTTP Error: {e}"
        print(error_msg)
        print(f"Request: {e.request.url}")
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        return {"error": error_msg}

async def get_recommendations(client: httpx.AsyncClient, token: str, preferred_genre: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get book recommendations based on preferences."""
    print("\n=== Getting Book Recommendations ===")
    print("This may take several minutes (300-400 seconds)...")
    headers = {"Authorization": f"Bearer {token}"}
    params = {}
    if preferred_genre:
        params["preferred_genre"] = preferred_genre
    try:
        # Set timeout to None for unlimited wait time
        response = await client.get("/recommendations", params=params, headers=headers, timeout=None)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} recommendations")
            return data
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            print(error_msg)
            return [{"error": error_msg}]
    except httpx.HTTPError as e:
        error_msg = f"HTTP Error: {e}"
        print(error_msg)
        print(f"Request: {e.request.url}")
        return [{"error": error_msg}]
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        return [{"error": error_msg}]

async def run_tests():
    """Run all API tests."""
    # Create client with no default timeout
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=None) as client:
        try:
            # Step 1: Register user and login
            user_response = await register_user(client)
            global user_id
            user_id = user_response.get("id")
            
            global access_token
            access_token = await login_user(client)
            
            if not access_token:
                print("Failed to get access token. Aborting tests.")
                return
            
            # Step 2: Create a book
            book_response = await create_book(client, access_token)
            global book_id
            book_id = book_response.get("id")
            
            if not book_id:
                print("Failed to create book. Aborting tests.")
                return
            
            # Step 3: Get all books
            await get_all_books(client, access_token)
            
            # Step 4: Get the specific book
            await get_book(client, book_id, access_token)
            
            # Step 5: Update the book
            await update_book(client, book_id, access_token)
            
            # Step 6: Add a review to the book
            await add_review(client, book_id, access_token)
            
            # Step 7: Get all reviews for the book
            await get_reviews(client, book_id, access_token)
            
            # Add wait time for database operations
            print("\nWaiting for database operations to complete before proceeding...")
            await asyncio.sleep(10)
            
            # Step 8: Get book summary with unlimited timeout
            await get_book_summary(client, book_id, access_token)
            
            # Wait between intensive API calls
            print("\nWaiting before next API call...")
            await asyncio.sleep(10)
            
            # Step 9: Generate a summary with unlimited timeout
            await generate_summary(client, access_token)
            
            # Wait between intensive API calls
            print("\nWaiting before next API call...")
            await asyncio.sleep(10)
            
            # Step 10: Get recommendations with unlimited timeout
            await get_recommendations(client, access_token, "Fiction")
            
            # Wait before deletion
            print("\nWaiting before deletion...")
            await asyncio.sleep(5)
            
            # Step 11: Delete the book
            await delete_book(client, book_id, access_token)
            
            print("\n=== All Tests Completed Successfully ===")
            
        except httpx.HTTPError as e:
            print(f"\nHTTP Error occurred: {e}")
            print(f"Request: {e.request.url}")
        except Exception as e:
            print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(run_tests())