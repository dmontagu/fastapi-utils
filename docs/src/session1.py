from pathlib import Path
from typing import Iterator
from uuid import UUID

import sqlalchemy as sa
from fastapi import Depends, FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from fastapi_utils.session import FastAPISessionMaker

Base = declarative_base()

# TODO: Read the database_uri from an environment variable by way of a BaseSettings subclass

class User(Base):
    __tablename__ = "user"
    id = sa.Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = sa.Column(sa.String, nullable=False)
    related_id = sa.Column(GUID)


sqlite_db_path = Path("./test.db")
database_uri = f"sqlite:///{sqlite_db_path}?check_same_thread=False"
session_maker = FastAPISessionMaker(database_uri=database_uri)


def get_db() -> Iterator[Session]:
    yield from session_maker.get_db()


app = FastAPI()


@app.get("/{user_id}")
def get_user_name(db: Session = Depends(get_db), *, user_id: UUID) -> str:
    user = db.query(User).get(user_id)
    username = user.name
    return username
