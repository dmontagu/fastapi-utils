from __future__ import annotations

import pytest
from fastapi import APIRouter, FastAPI

with pytest.warns(DeprecationWarning):
    from fastapi_utils.inferring_router import InferringRouter

openapi_spec = {
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "openapi": "3.0.2",
    "paths": {
        "/1": {
            "get": {
                "operationId": "endpoint_1_1_get",
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {"schema": {"title": "Response " "Endpoint 1 1 Get", "type": "string"}}
                        },
                        "description": "Successful " "Response",
                    }
                },
                "summary": "Endpoint 1",
            }
        },
        "/2": {
            "get": {
                "operationId": "endpoint_2_2_get",
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {"schema": {"title": "Response " "Endpoint 2 2 Get", "type": "integer"}}
                        },
                        "description": "Successful " "Response",
                    }
                },
                "summary": "Endpoint 2",
            }
        },
    },
}


@pytest.mark.parametrize("Router", [InferringRouter, APIRouter])
def test_inferring_router(Router: type[InferringRouter] | type[APIRouter]) -> None:
    inferring_router = Router()

    @inferring_router.get("/1")
    def endpoint_1() -> str:  # pragma: no cover
        return ""

    @inferring_router.get("/2", response_model=int)
    def endpoint_2() -> str:  # pragma: no cover
        return ""

    app = FastAPI()
    app.include_router(inferring_router)
    assert app.openapi() == openapi_spec
