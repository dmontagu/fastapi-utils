from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from uuid import UUID

import pytest
import sqlalchemy as sa
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session, declarative_base  # type: ignore[attr-defined]

from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from fastapi_utils.session import FastAPISessionMaker, get_engine

Base = declarative_base()


class User(Base):  # type: ignore[valid-type,misc]
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
    user = db.get(User, user_id)  # type: ignore[attr-defined]
    username = user.name
    return username


@pytest.fixture(scope="module")
def test_app() -> Iterator[FastAPI]:
    if test_db_path.exists():
        test_db_path.unlink()

    engine = get_engine(database_uri)
    Base.metadata.create_all(bind=engine)

    yield app
    if test_db_path.exists():
        test_db_path.unlink()
