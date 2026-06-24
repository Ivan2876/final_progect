from pydantic import BaseModel, Field
from datetime import datetime

class TravelPriceWhenSchema(BaseModel):
    price: float = Field(ge=1)
    when: float = Field(examples=[23062026])

class TravelCrateSchema(TravelPriceWhenSchema):
    name: str = Field(examples=['Перемишель, Кошалін'])
    author: str = Field(examples=['Річард Метісон'])

class TravelSavedSchema(TravelCrateSchema):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)