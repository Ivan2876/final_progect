from fastapi import APIRouter, status, Query
from final_progect_shemas import TravelPriceWhenSchema, TravelCrateSchema, TravelSavedSchema
from final_progect_storage import storage

api_router = APIRouter(
    prefix='/api/travels'
)

@api_router.post("", status_code=status.HTTP_201_CREATED)
def create_travel(travel: TravelCrateSchema) -> TravelSavedSchema:
    saved_travel = storage.create_travel(travel)

    return saved_travel

@api_router.get("/{travel_id}")
def get_travel(travel_id: str) -> TravelSavedSchema:
    saved_travel = storage.get_travel(travel_id)

    return saved_travel


@api_router.get("")
def get_travels(
        page: int = Query(default=1, ge=1),
        q: str = Query(default=''),
) -> list[TravelSavedSchema]:
    saved_travels = storage.get_travels(q, page=page)

    return saved_travels


@api_router.delete("/{travel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_travel(travel_id: str) -> None:
    storage.delete_travel(travel_id)


@api_router.patch("/{travel_id}")
def patch_travel(travel_id: str, new_travel_data: TravelPriceWhenSchema) -> TravelSavedSchema:
    patched_travel = storage.update_travel(travel_id, new_travel_data)

    return patched_travel


@api_router.put("/{travel_id}")
def put_travel(travel_id: str, travel: TravelCrateSchema) -> TravelSavedSchema:
    put_travel_obj = storage.update_travel(travel_id, travel)

    return put_travel_obj
