from typing import ClassVar

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
