from __future__ import annotations

import pydantic
import pytest
from fastapi import Depends, FastAPI
from starlette.testclient import TestClient

from fastapi_utils.pagination import LimitOffsetParams, Page, paginate

PYDANTIC_VERSION = pydantic.VERSION


def model_dump_by_alias(model: Page[int]) -> dict[str, object]:
    if PYDANTIC_VERSION[0] == "2":
        return model.model_dump(by_alias=True)
    return model.dict(by_alias=True)


def test_paginate_first_page() -> None:
    params = LimitOffsetParams(limit=2, offset=0)

    page = paginate([1, 2], total=5, params=params)

    assert page.items == [1, 2]
    assert page.total == 5
    assert page.limit == 2
    assert page.offset == 0
    assert page.next_offset == 2
    assert page.previous_offset is None


def test_paginate_middle_page() -> None:
    params = LimitOffsetParams(limit=2, offset=2)

    page = paginate([3, 4], total=5, params=params)

    assert page.next_offset == 4
    assert page.previous_offset == 0


def test_paginate_last_page() -> None:
    params = LimitOffsetParams(limit=2, offset=4)

    page = paginate([5], total=5, params=params)

    assert page.next_offset is None
    assert page.previous_offset == 2


def test_paginate_previous_offset_does_not_go_below_zero() -> None:
    params = LimitOffsetParams(limit=50, offset=20)

    page = paginate([1], total=100, params=params)

    assert page.previous_offset == 0


def test_paginate_rejects_negative_total() -> None:
    params = LimitOffsetParams()

    with pytest.raises(ValueError, match="total"):
        paginate([], total=-1, params=params)


def test_limit_offset_params_can_be_constructed_without_fastapi() -> None:
    params = LimitOffsetParams()

    assert params.limit == 50
    assert params.offset == 0


def test_limit_offset_params_validate_direct_values() -> None:
    with pytest.raises(ValueError, match="limit"):
        LimitOffsetParams(limit=0)

    with pytest.raises(ValueError, match="limit"):
        LimitOffsetParams(limit=101)

    with pytest.raises(ValueError, match="offset"):
        LimitOffsetParams(offset=-1)


def test_page_uses_camel_case_aliases() -> None:
    page = Page[int](
        items=[1],
        total=2,
        limit=1,
        offset=0,
        next_offset=1,
        previous_offset=None,
    )

    dumped = model_dump_by_alias(page)

    assert dumped["nextOffset"] == 1
    assert dumped["previousOffset"] is None


def test_limit_offset_params_work_as_fastapi_dependency() -> None:
    app = FastAPI()
    values = [1, 2, 3, 4]

    @app.get("/items", response_model=Page[int])
    def list_items(params: LimitOffsetParams = Depends()) -> Page[int]:
        return paginate(
            values[params.offset : params.offset + params.limit],
            total=len(values),
            params=params,
        )

    response = TestClient(app).get("/items?limit=2&offset=1")

    assert response.status_code == 200
    assert response.json() == {
        "items": [2, 3],
        "total": 4,
        "limit": 2,
        "offset": 1,
        "nextOffset": 3,
        "previousOffset": 0,
    }
