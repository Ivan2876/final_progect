from fastapi import APIRouter, status, Query
from schemas import BookCreateSchema, BookSavedSchema

from storage import storage

api_router = APIRouter(
    prefix='/api/books'
)

@api_router.post("", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema) -> BookSavedSchema:
    saved_book = storage.create_book(book)

    return saved_book


@api_router.get("/{book_id}")
def get_book(book_id: str) -> BookSavedSchema:
    saved_book = storage.get_book(book_id)

    return saved_book


@api_router.get("")
def get_books(
        page: int = Query(default=1, ge=1),
        q: str = Query(default=''),
) -> list[BookSavedSchema]:
    saved_books = storage.get_books(q, page=page)

    return saved_books