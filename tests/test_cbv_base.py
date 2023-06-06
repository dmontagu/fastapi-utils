from typing import Any, Dict, List, Union

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.testclient import TestClient

from fastapi_restful.cbv_base import Api, Resource, set_responses


def test_cbv() -> None:
    class CBV(Resource):
        def __init__(self, z: int = 1):
            super().__init__()
            self.y = 1
            self.z = z

        @set_responses(int)
        def post(self, x: int) -> int:
            print(x)
            return x + self.y + self.z

        @set_responses(bool)
        def get(self) -> bool:
            return hasattr(self, "cy")

    app = FastAPI()
    api = Api(app)
    cbv = CBV(2)
    api.add_resource(cbv, "/", "/classvar")

    client = TestClient(app)
    response_1 = client.post("/", params={"x": 1}, json={})
    assert response_1.status_code == 200
    assert response_1.content == b"4"

    response_2 = client.get("/classvar")
    assert response_2.status_code == 200
    assert response_2.content == b"false"


def test_arg_in_path() -> None:
    class TestCBV(Resource):
        @set_responses(str)
        def get(self, item_id: str) -> str:
            return item_id

    app = FastAPI()
    api = Api(app)

    test_cbv_resource = TestCBV()
    api.add_resource(test_cbv_resource, "/{item_id}")

    assert TestClient(app).get("/test").json() == "test"


def test_multiple_routes() -> None:
    class RootHandler(Resource):
        def get(self, item_path: str | None = None) -> Union[List[Any], Dict[str, str]]:
            if item_path:
                return {"item_path": item_path}
            return []

    app = FastAPI()
    api = Api(app)

    root_handler_resource = RootHandler()
    api.add_resource(root_handler_resource, "/items/?", "/items/{item_path:path}")

    client = TestClient(app)

    assert client.get("/items/1").json() == {"item_path": "1"}
    assert client.get("/items").json() == []


def test_different_response_model() -> None:
    class RootHandler(Resource):
        @set_responses({}, response_class=PlainTextResponse)
        def get(self) -> str:
            return "Done!"

    app = FastAPI()
    api = Api(app)

    api.add_resource(RootHandler(), "/check")

    client = TestClient(app)

    assert client.get("/check").text == "Done!"
