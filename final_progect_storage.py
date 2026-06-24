from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from abc import ABC, abstractmethod

from final_progect_shemas import TravelPriceWhenSchema, TravelCrateSchema, TravelSavedSchema
from settings import settings

class BaseStorage(ABC):
    @abstractmethod
    def create_travel(self, travel: TravelCrateSchema) -> TravelSavedSchema:
        pass

    @abstractmethod
    def update_travel(self, travel_id: str, new_travel_data: TravelPriceWhenSchema | TravelCrateSchema) -> TravelSavedSchema:
        pass

    @abstractmethod
    def get_travel(self, travel_id: str) -> TravelSavedSchema:
        pass

    @abstractmethod
    def delete_travel(self, travel_id: str) -> None:
        pass

    @abstractmethod
    def get_travels(self, q: str = "", page: int = 1)-> list[TravelSavedSchema]:
        pass

class MongoDBStorage(BaseStorage):
    def __init__(self):
        client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
        db = client[settings.MONGO_DB]
        self.collection = db[settings.MONGO_COLLECTION]

    def create_travel(self, travel: TravelCrateSchema) -> TravelSavedSchema:
        travel_dict = travel.model_dump()
        travel_dict['created_at'] = datetime.now()
        saved_travel_in_db = self.collection.insert_one(travel_dict)

        saved_travel = self.get_travel(saved_travel_in_db.inserted_id)

        return saved_travel

    def update_travel(self, travel_id: str, new_travel_data: TravelPriceWhenSchema | TravelCrateSchema) -> TravelSavedSchema:
        payload = {'$set': new_travel_data.model_dump()}
        result = self.collection.update_one(self._get_object_id_query(travel_id), payload)
        if not result.raw_result['n']:
            raise HTTPException(
                detail=f'travel with id={travel_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        saved_travel = self.get_travel(travel_id)
        return saved_travel

    def _get_object_id_query(self, travel_id: str) -> dict[str, ObjectId]:
        try:
            query = {"_id": ObjectId(travel_id)}
            return query
        except InvalidId:
            raise HTTPException(
                detail=f"Invalid travel id {travel_id}",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def get_travel(self, travel_id: str) -> TravelSavedSchema:
        travel = self.collection.find_one(self._get_object_id_query(travel_id))
        if not travel:
            raise HTTPException(
                detail=f'travel with id={travel_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        travel = self.transform_travel(travel)

        return travel

    def delete_travel(self, travel_id: str) -> None:
        self.get_travel(travel_id)
        self.collection.delete_one(self._get_object_id_query(travel_id))

    def transform_travel(self, travel: dict) -> TravelSavedSchema:
        travel = TravelSavedSchema(
            name=travel['name'],
            when=travel['when'],
            price=travel['price'],
            author=travel['author'],
            id=str(travel['_id']),
            created_at=travel['created_at'],
        )
        return travel


    def get_travels(self, q: str = "", page: int = 1)-> list[TravelSavedSchema]:
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
        travels = self.collection.find(query).limit(settings.PAGE_SIZE).skip(skip)
        saved_travels = []
        for travel in travels:
            saved_travels.append(self.transform_travel(travel))

        return saved_travels

storage: BaseStorage = MongoDBStorage()