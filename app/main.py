from datetime import timedelta
from typing import Annotated

from bson.objectid import ObjectId
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.extensions.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
)
from app.extensions.database import db
from app.schemas import MovieSchema, TokenSchema, UserCreateSchema, UserResponseSchema
from app.serializers import movieEntity, movieListEntity, userEntity

app = FastAPI()

Movie = db.movies
User = db.users

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# cors
@app.post("/api/createuser", response_model=UserResponseSchema)
async def create_user(user: UserCreateSchema):
    queried_user = await User.find_one({"username": user.username})
    if queried_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that username already exists",
        )
    hashed_password = get_password_hash(user.password)
    user_db = await User.insert_one(
        {"username": user.username, "hashed_password": hashed_password, "active": True}
    )
    user_db = await User.find_one({"_id": user_db.inserted_id})
    user_db = userEntity(user_db)
    return user_db


@app.post("/api/token", response_model=TokenSchema)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """login"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.get("username")}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    "/api/movies", response_model=list[MovieSchema], status_code=status.HTTP_200_OK
)
async def get_movies(
    current_user: Annotated[str, Depends(get_current_user)],
    title: str | None = None,
    sort: str | None = None,
):
    """Retrieve movies"""
    if title and not sort:
        movies = await Movie.find(
            {"title": {"$regex": title, "$options": "i"}}
        ).to_list(50)
    elif sort == "title" and not title:
        movies = await Movie.find().sort(sort).to_list(50)
    elif sort == "rating" and not title:
        movies = await Movie.find().sort(sort, -1).to_list(50)
    elif title and sort == "title":
        movies = (
            await Movie.find({"title": {"$regex": title, "$options": "i"}})
            .sort(sort)
            .to_list(50)
        )
    elif title and sort == "rating":
        movies = (
            await Movie.find({"title": {"$regex": title, "$options": "i"}})
            .sort(sort, -1)
            .to_list(50)
        )
    else:
        movies = await Movie.find().to_list(50)
    return movieListEntity(movies)


@app.get("/api/movies/{id}", response_model=MovieSchema, status_code=status.HTTP_200_OK)
async def get_movie_by_id(
    id: str,
    current_user: Annotated[str, Depends(get_current_user)],
):
    """Retrieve specific movie by id"""
    movie = await Movie.find_one({"_id": ObjectId(id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie = movieEntity(movie)
    return movie
