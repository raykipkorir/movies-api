from bson.objectid import ObjectId
from pydantic import BaseModel


class Movie(BaseModel):
    id: str
    title: str
    rating: int
    url: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
