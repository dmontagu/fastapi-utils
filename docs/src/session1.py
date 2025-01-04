from functools import lru_cache
from typing import Iterator
from uuid import UUID

import sqlalchemy as sa
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseSettings
from sqlalchemy.orm import Session, declarative_base

from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from fastapi_utils.session import FastAPISessionMaker

Base = declarative_base()

# Define a simple User model to demonstrate usage
class User(Base):
    __tablename__ = "user"
    id = sa.Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = sa.Column(sa.String, nullable=False)

class DBSettings(BaseSettings):
    """Parses variables from environment on instantiation"""
    # This will automatically load the database URI from environment variables or a config file
    database_uri: str  # This should contain the URI of the database (e.g., 'postgresql://user:password@localhost/dbname')

    class Config:
        # Optional: this specifies the file that contains the environment variables (e.g., `.env` file)
        env_file = ".env"  # If you have an .env file, it will load from there automatically

def get_db() -> Iterator[Session]:
    """FastAPI dependency that provides a SQLAlchemy session"""
    yield from _get_fastapi_sessionmaker().get_db()

@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """Initializes the FastAPISessionMaker with the database URI fetched from the environment"""
    # Fetch the database URI using DBSettings (it automatically reads from environment variables)
    database_uri = DBSettings().database_uri
    return FastAPISessionMaker(database_uri)

app = FastAPI()

@app.get("/{user_id}")
def get_user_name(db: Session = Depends(get_db), *, user_id: UUID) -> str:
    """Fetch user by ID from the database"""
    user = db.get(User, user_id)  # Retrieve the user from the database by ID
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.name
