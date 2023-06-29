def movieEntity(movie) -> dict:
    return {
        "id": str(movie["_id"]),
        "title": movie["title"],
        "rating": movie["rating"],
        "url": movie["url"],
    }


def movieListEntity(movies) -> list:
    return [movieEntity(movie) for movie in movies]
