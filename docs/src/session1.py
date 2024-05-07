from functools import lru_cache
from typing import Iterator
from uuid import UUID

import sqlalchemy as sa
from fastapi import Depends, FastAPI
from pydantic import BaseSettings
from sqlalchemy.orm import Session, declarative_base

from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from fastapi_utils.session import FastAPISessionMaker

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = sa.Column(sa.String, nullable=False)


class DBSettings(BaseSettings):
    """Parses variables from environment on instantiation"""

    database_uri: str  # could break up into scheme, username, password, host, db


def get_db() -> Iterator[Session]:
    """FastAPI dependency that provides a sqlalchemy session"""
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """This function could be replaced with a global variable if preferred"""
    database_uri = DBSettings().database_uri
    return FastAPISessionMaker(database_uri)


app = FastAPI()


@app.get("/{user_id}")
def get_user_name(db: Session = Depends(get_db), *, user_id: UUID) -> str:
    user = db.get(User, user_id)
    username = user.name
    return username
