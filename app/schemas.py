from bson.objectid import ObjectId
from pydantic import BaseModel


class MovieSchema(BaseModel):
    id: str
    title: str
    rating: int
    url: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserResponseSchema(BaseModel):
    username: str
    active: bool


class UserCreateSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
