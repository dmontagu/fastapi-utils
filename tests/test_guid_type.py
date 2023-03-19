from __future__ import annotations

import uuid

from fastapi import FastAPI
from starlette.testclient import TestClient

from fastapi_utils.session import context_session
from tests.conftest import User, session_maker


def test_guid(test_app: FastAPI) -> None:
    name1 = "test_name_1"
    name2 = "test_name_2"
    user_id_1 = str(uuid.uuid4())

    with context_session(session_maker.cached_engine) as session:
        user1 = User(id=user_id_1, name=name1)
        session.add(user1)
        session.commit()
        assert str(user1.id) == user_id_1
        assert user1.related_id is None

    with session_maker.context_session() as session:
        user2 = User(name=name2)
        assert user2.id is None
        session.add(user2)
        session.commit()
        user_id_2 = user2.id
        assert user_id_2 is not None
        assert user2.related_id is None

    test_client = TestClient(test_app)
    assert test_client.get(f"/{user_id_1}").json() == name1
    assert test_client.get(f"/{user_id_2}").json() == name2
