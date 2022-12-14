from typing import List

from pydantic import BaseModel


class Artist(BaseModel):
    id: str
    name: str
    n_followers: int
    genres: List[str]
    popularity: float


class Playlist(BaseModel):
    id: str
    name: str
    description: str
    url: str


class Track(BaseModel):
    id: str
    name: str
    popularity: float
    artists_id: List[str]
