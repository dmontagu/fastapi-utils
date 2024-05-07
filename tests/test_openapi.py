from __future__ import annotations

import pytest
from fastapi import FastAPI

from fastapi_utils.openapi import simplify_operation_ids


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()

    @app.get("/endpoint-path")
    def endpoint_name() -> str:  # pragma: no cover
        return ""

    return app


def test_base_spec(app: FastAPI) -> None:
    assert app.openapi()["paths"]["/endpoint-path"]["get"]["operationId"] == "endpoint_name_endpoint_path_get"


def test_simplify_spec(app: FastAPI) -> None:
    simplify_operation_ids(app)
    assert app.openapi()["paths"]["/endpoint-path"]["get"]["operationId"] == "endpoint_name"
