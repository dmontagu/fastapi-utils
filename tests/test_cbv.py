from __future__ import annotations

import pytest
from fastapi import APIRouter, Depends
from starlette.testclient import TestClient
from typing import Any, ClassVar

from fastapi_restful.cbv import cbv


class TestCBV:
    @pytest.fixture(autouse=True)
    def router(self) -> APIRouter:
        return APIRouter()

    def test_response_models(self, router: APIRouter) -> None:
        expected_response = "home"

        @cbv(router)
        class CBV:
            def __init__(self) -> None:
                self.one = 1
                self.two = 2

            @router.get("/", response_model=str)
            def string_response(self) -> str:
                return expected_response

            @router.get("/sum", response_model=int)
            def int_response(self) -> int:
                return self.one + self.two

        client = TestClient(router)
        response_1 = client.get("/")
        assert response_1.status_code == 200
        assert response_1.json() == expected_response

        response_2 = client.get("/sum")
        assert response_2.status_code == 200
        assert response_2.content == b"3"

    def test_dependencies(self, router: APIRouter) -> None:
        def dependency_one() -> int:
            return 1

        def dependency_two() -> int:
            return 2

        @cbv(router)
        class CBV:
            one: int = Depends(dependency_one)

            def __init__(self, two: int = Depends(dependency_two)):
                self.two = two

            @router.get("/", response_model=int)
            def int_dependencies(self) -> int:
                return self.one + self.two

        client = TestClient(router)
        response = client.get("/")
        assert response.status_code == 200
        assert response.content == b"3"

    def test_class_var(self, router: APIRouter) -> None:
        @cbv(router)
        class CBV:
            class_var: ClassVar[int]

            @router.get("/", response_model=bool)
            def g(self) -> bool:
                return hasattr(self, "class_var")

        client = TestClient(router)
        response = client.get("/")
        assert response.status_code == 200
        assert response.content == b"false"

    def test_routes_path_order_preserved(self, router: APIRouter) -> None:
        @cbv(router)
        class CBV:
            @router.get("/test")
            def get_test(self) -> int:
                return 1

            @router.get("/{any_path}")
            def get_any_path(self) -> int:  # Alphabetically before `get_test`
                return 2

        client = TestClient(router)
        assert client.get("/test").json() == 1
        assert client.get("/any_other_path").json() == 2

    def test_multiple_paths(self, router: APIRouter) -> None:
        @cbv(router)
        class CBV:
            @router.get("/items")
            @router.get("/items/{custom_path:path}")
            @router.get("/database/{custom_path:path}")
            def root(self, custom_path: str = None) -> Any:
                return {"custom_path": custom_path} if custom_path else []

        client = TestClient(router)
        assert client.get("/items").json() == []
        assert client.get("/items/1").json() == {"custom_path": "1"}
        assert client.get("/database/abc").json() == {"custom_path": "abc"}

    def test_query_parameters(self, router: APIRouter) -> None:
        @cbv(router)
        class CBV:
            @router.get("/route")
            def root(self, param: int = None) -> int:
                return param if param else 0

        client = TestClient(router)
        assert client.get("/route").json() == 0
        assert client.get("/route?param=3").json() == 3

    def test_prefix(self) -> None:
        router = APIRouter(prefix="/api")

        @cbv(router)
        class CBV:
            @router.get("/item")
            def root(self) -> str:
                return "hello"

        client = TestClient(router)
        response = client.get("/api/item")
        assert response.status_code == 200
        assert response.json() == "hello"
