from typing import Annotated

from bson.objectid import ObjectId
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database import db
from app.schemas import Movie
from app.serializers import movieEntity, movieListEntity

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# jwt tokens, cors
@app.get("/api/movies", response_model=list[Movie], status_code=status.HTTP_200_OK)
async def get_movies( token: Annotated[str, Depends(oauth2_scheme)], title: str | None = None, sort: str | None = None):
    """Retrieve movies"""
    if title and not sort:
        movies = await db.movies.find({"title": {"$regex": title, "$options": "i"}}).to_list(50)
    elif sort=="title" and not title:
        movies = await db.movies.find().sort(sort).to_list(50)
    elif sort=="rating" and not title:
        movies = await db.movies.find().sort(sort, -1).to_list(50)
    elif title and sort=="title":
        movies = await db.movies.find({"title": {"$regex": title, "$options": "i"}}).sort(sort).to_list(50)
    elif title and sort=="rating":
        movies = await db.movies.find({"title": {"$regex": title, "$options": "i"}}).sort(sort, -1).to_list(50)
    else:
        movies = await db.movies.find().to_list(50)
    print(token)
    return movieListEntity(movies)


@app.get("/api/movies/{id}", response_model=Movie,  status_code=status.HTTP_200_OK)
async def get_movie_by_id(id: str):
    """Retrieve specific movie by id"""
    movie = await db.movies.find_one({"_id": ObjectId(id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie = movieEntity(movie)
    return movie
