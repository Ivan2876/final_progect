from pydantic import BaseModel, Field
from datetime import datetime


class BookPriceImageSchema(BaseModel):
    price: float = Field(ge=1)
    image: str = Field(examples=['https://upload.wikimedia.org/wikipedia/uk/1/18/I_Am_Legend_%28ukr_poster%29.jpg'])


class BookCreateSchema(BookPriceImageSchema):
    title: str = Field(examples=['Я, легенда'])
    author: str = Field(examples=['Річард Метісон'])


class BookSavedSchema(BookCreateSchema):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
