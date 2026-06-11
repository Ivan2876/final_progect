from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId

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
        print(saved_book_in_db.inserted_id)

        saved_book = self.get_book(saved_book_in_db.inserted_id)

        return saved_book

    def get_book(self, book_id) -> BookSavedSchema:
        query = {"_id": ObjectId(book_id)}
        book = self.collection.find_one(query)
        book = BookSavedSchema(
            title=book['title'],
            image=book['image'],
            price=book['price'],
            author=book['author'],
            id=str(book['_id']),
            created_at=book['created_at'],
        )

        return book

storage = MongoDBStorage()
