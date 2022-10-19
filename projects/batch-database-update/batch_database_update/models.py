from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Artist(Base):  # type: ignore
    __tablename__ = "artists"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    n_followers = Column(Integer, nullable=False)
    popularity = Column(Float, nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=False)
