from __future__ import annotations

from typing import Any, ClassVar, Optional

from fastapi import APIRouter, Depends, FastAPI
from starlette.testclient import TestClient

from fastapi_utils.cbv import cbv


def test_cbv() -> None:
    router = APIRouter()

    def dependency() -> int:
        return 1

    @cbv(router)
    class CBV:
        x: int = Depends(dependency)
        cx: ClassVar[int] = 1
        cy: ClassVar[int]

        def __init__(self, z: int = Depends(dependency)):
            self.y = 1
            self.z = z

        @router.get("/", response_model=int)
        def f(self) -> int:
            return self.cx + self.x + self.y + self.z

        @router.get("/classvar", response_model=bool)
        def g(self) -> bool:
            return hasattr(self, "cy")

    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    response_1 = client.get("/")
    assert response_1.status_code == 200
    assert response_1.content == b"4"

    response_2 = client.get("/classvar")
    assert response_2.status_code == 200
    assert response_2.content == b"false"


def test_method_order_preserved() -> None:
    router = APIRouter()

    @cbv(router)
    class TestCBV:
        @router.get("/test")
        def get_test(self) -> int:
            return 1

        @router.get("/{item_id}")
        def get_item(self) -> int:  # Alphabetically before `get_test`
            return 2

    app = FastAPI()
    app.include_router(router)

    assert TestClient(app).get("/test").json() == 1
    assert TestClient(app).get("/other").json() == 2


def test_multiple_decorators() -> None:
    router = APIRouter()

    @cbv(router)
    class RootHandler:
        @router.get("/items/?")
        @router.get("/items/{item_path:path}")
        @router.get("/database/{item_path:path}")
        def root(self, item_path: Optional[str] = None, item_query: Optional[str] = None) -> Any:
            if item_path:
                return {"item_path": item_path}
            if item_query:
                return {"item_query": item_query}
            return []

    client = TestClient(router)

    assert client.get("/items").json() == []
    assert client.get("/items/1").json() == {"item_path": "1"}
    assert client.get("/database/abc").json() == {"item_path": "abc"}
