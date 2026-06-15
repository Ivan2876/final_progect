from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status

from schemas import BookCreateSchema, BookSavedSchema
from settings import settings


class MongoDBStorage:
    def __init__(self):
        client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
        db = client[settings.MONGO_DB]
        self.collection = db[settings.MONGO_COLLECTION]

    def create_book(self, book: BookCreateSchema) -> BookSavedSchema:
        book_dict = book.model_dump()
        book_dict['created_at'] = datetime.now()
        saved_book_in_db = self.collection.insert_one(book_dict)

        saved_book = self.get_book(saved_book_in_db.inserted_id)

        return saved_book

    def get_book(self, book_id: str) -> BookSavedSchema:
        try:
            query = {"_id": ObjectId(book_id)}
        except InvalidId:
            raise HTTPException(
                detail=f"Invalid book id {book_id}",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        book = self.collection.find_one(query)
        if not book:
            raise HTTPException(
                detail=f'Book with id={book_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        book = self.transform_book(book)

        return book

    def transform_book(self, book: dict) -> BookSavedSchema:
        book = BookSavedSchema(
            title=book['title'],
            image=book['image'],
            price=book['price'],
            author=book['author'],
            id=str(book['_id']),
            created_at=book['created_at'],
        )
        return book


    def get_books(self, q: str = "", page: int = 1)-> list[BookSavedSchema]:
        query = {}
        if q:
            query_words = q.split()
            print(query_words)

            # target_list = []
            # for word in query_words:
            #     if len(word) > 1:
            #         target_list.append(word.lower())
            query_words = [word.lower() for word in query_words if len(word) > 1]

            if query_words:
                query_words_dicts = [{'title': {"$regex": word, "$options": 'i'}} for word in query_words]
                query = {
                    "$and": query_words_dicts
                }
        skip = (page - 1) *  settings.PAGE_SIZE
        books = self.collection.find(query).limit(settings.PAGE_SIZE).skip(skip)
        saved_books = []
        for book in books:
            saved_books.append(self.transform_book(book))

        return saved_books



storage = MongoDBStorage()