from fastapi import APIRouter, status, Query
from schemas import BookCreateSchema, BookSavedSchema, BookPriceImageSchema

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


@api_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str) -> None:
    storage.delete_book(book_id)


@api_router.patch("/{book_id}")
def patch_book(book_id: str, new_book_data: BookPriceImageSchema) -> BookSavedSchema:
    patched_book = storage.update_book(book_id, new_book_data)

    return patched_book


@api_router.put("/{book_id}")
def put_book(book_id: str, book: BookCreateSchema) -> BookSavedSchema:
    put_book_obj = storage.update_book(book_id, book)

    return put_book_obj