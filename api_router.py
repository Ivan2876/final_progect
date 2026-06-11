from schemas import BookCreateSchema, BookSavedSchema
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from storage import storage

api_router = APIRouter(
    prefix='/api/books'
)

@api_router.post("", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema) -> BookSavedSchema:
    saved_book = storage.create_book(book)
    return saved_book