from __future__ import annotations

from typing import Any, Dict

import pytest
from fastapi import FastAPI

with pytest.warns(DeprecationWarning):
    from fastapi_utils.inferring_router import InferringRouter

OpenapiSchemaType = Dict[str, Any]


def get_response_schema(
    openapi_spec: OpenapiSchemaType, endpoint_path: str, expected_status_code: int = 200
) -> OpenapiSchemaType:
    responses = openapi_spec["paths"][endpoint_path]["get"]["responses"]
    content = responses[str(expected_status_code)].get("content")
    return content["application/json"]["schema"] if content else content


class TestInferringRouter:
    @pytest.fixture()
    def app(self) -> FastAPI:
        return FastAPI()

    @pytest.fixture()
    def inferring_router(self) -> InferringRouter:
        return InferringRouter()

    def test_inferring_route(self, app: FastAPI, inferring_router: InferringRouter) -> None:
        @inferring_router.get("/return_string")
        def endpoint_1() -> str:  # pragma: no cover
            return ""

        @inferring_router.get("/return_integer", response_model=int)
        def endpoint_2() -> int:  # pragma: no cover
            return 0

        app.include_router(inferring_router)
        openapi_spec = app.openapi()
        assert get_response_schema(openapi_spec, "/return_string")["type"] == "string"
        assert get_response_schema(openapi_spec, "/return_integer")["type"] == "integer"
