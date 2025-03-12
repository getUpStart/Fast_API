import json
from fastapi import Body, FastAPI

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOK = [
    Book(1, "Science", "Adam", "depth in science", 3),
    Book(2, "Math", "Alex", "depth in math", 5),
    Book(3, "History", "Alex", "depth in history", 2),
    Book(4, "AI", "zenith", "depth in AI", 3),
    Book(5, "Computer", "Peter", "depth in computer", 4),
]
    
app = FastAPI()

@app.get("/books")
async def get_all_book():
    return BOOK

@app.post("/books")
async def add_book(book = Body()):
    return BOOK.append(book)