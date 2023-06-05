from pathlib import Path
from typing import Iterator
from uuid import UUID

import pytest
import sqlalchemy as sa
from fastapi import Depends, FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from fastapi_restful.guid_type import GUID, GUID_DEFAULT_SQLITE
from fastapi_restful.session import FastAPISessionMaker, get_engine

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = sa.Column(sa.String, nullable=False)
    related_id = sa.Column(GUID)


test_db_path = Path("./test.db")
database_uri = f"sqlite:///{test_db_path}?check_same_thread=False"
session_maker = FastAPISessionMaker(database_uri=database_uri)


def get_db() -> Iterator[Session]:
    yield from session_maker.get_db()


app = FastAPI()


@app.get("/{user_id}")
def get_user_name(db: Session = Depends(get_db), *, user_id: UUID) -> str:
    user = db.query(User).get(user_id)
    if isinstance(user, User):
        username = user.name
        return username
    return ""


@pytest.fixture(scope="module")
def test_app() -> Iterator[FastAPI]:
    if test_db_path.exists():
        test_db_path.unlink()

    engine = get_engine(database_uri)
    Base.metadata.create_all(bind=engine)

    yield app
    if test_db_path.exists():
        test_db_path.unlink()
