from typing import Optional

from fastapi import APIRouter, Depends, FastAPI
from starlette.testclient import TestClient

from fastapi_utils.cbv import cbv, generic_cbv


def get_a(a: int) -> int:
    return a


def get_double_b(b: int) -> int:
    return 2 * b


def get_string(c: Optional[str] = None) -> Optional[str]:
    return c


router = APIRouter()


@generic_cbv(router)
class BaseGenericCBV:
    number: int = Depends(None)

    @router.get("/")
    async def echo_number(self) -> int:
        return self.number


other_router = APIRouter()


@generic_cbv(other_router)
class GenericCBV(BaseGenericCBV):
    string: Optional[str] = Depends(None)

    @router.get("/string")
    async def echo_string(self) -> Optional[str]:
        return self.string


router_a = APIRouter()
router_b = APIRouter()


@cbv(router_a)
class CBVA(GenericCBV):
    number = Depends(get_a)
    string = Depends(get_string)


@cbv(router_b)
class CBVB(GenericCBV):
    number = Depends(get_double_b)
    string = Depends(get_string)


app = FastAPI()
app.include_router(router_a, prefix="/a")
app.include_router(router_b, prefix="/b")


def test_generic_cbv() -> None:
    assert TestClient(app).get("/a/", params={"a": 1}).json() == 1
    assert TestClient(app).get("/b/", params={"b": 1}).json() == 2

    assert TestClient(app).get("/a/string", params={"a": 1, "c": "hello"}).json() == "hello"
    assert TestClient(app).get("/b/string", params={"b": 1, "c": "world"}).json() == "world"
