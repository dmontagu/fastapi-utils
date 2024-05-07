from __future__ import annotations

from dataclasses import dataclass

import pydantic

from fastapi_utils.api_model import APIModel

PYDANTIC_VERSION = pydantic.VERSION


def test_orm_mode() -> None:
    @dataclass
    class Data:
        x: int

    class Model(APIModel):
        x: int

        model_config = {"from_attributes": True}

    if PYDANTIC_VERSION[0] == "2":
        assert Model.model_validate(Data(x=1)).x == 1
    else:
        assert Model.from_orm(Data(x=1)).x == 1


def test_aliases() -> None:
    class Model(APIModel):
        some_field: str

    assert Model(some_field="a").some_field == "a"
    assert Model(someField="a").some_field == "a"  # type: ignore[call-arg]
