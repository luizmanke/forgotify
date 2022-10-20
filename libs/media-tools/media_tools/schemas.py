from pydantic import BaseModel


class Artist(BaseModel):
    id: str
    name: str
    n_followers: int
    genres: list
    popularity: float
