from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Artist(Base):  # type: ignore
    __tablename__ = "artists"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    n_followers = Column(Integer, nullable=False)
    popularity = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class ArtistToTrack(Base):  # type: ignore
    __tablename__ = "artists_to_tracks"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    artist_id = Column(String, nullable=False)
    track_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


class Track(Base):  # type: ignore
    __tablename__ = "tracks"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    popularity = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
