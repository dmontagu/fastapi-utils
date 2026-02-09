from __future__ import annotations

from dataclasses import dataclass

from fastapi_utils.api_model import APIModel
from fastapi_utils.api_model import APIMessage, PYDANTIC_VERSION
from pytest import MonkeyPatch  # type: ignore[import]


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
        assert Model.from_orm(Data(x=1)).x == 1  # type: ignore[reportDeprecated]


def test_aliases() -> None:
    class Model(APIModel):
        some_field: str

    assert Model(some_field="a").some_field == "a"
    assert Model(someField="a").some_field == "a"  # type: ignore[reportMissingParameter]


def test_alias_population_and_serialization() -> None:
    class Model(APIModel):
        some_field: str

    m_alias = Model(someField="alias")  # type: ignore[reportMissingParameter]
    m_field = Model(some_field="field")

    assert m_alias.some_field == "alias"
    assert m_field.some_field == "field"

    if PYDANTIC_VERSION[0] == "2":
        alias_dump = m_alias.model_dump(by_alias=True)
        field_dump = m_alias.model_dump()
    else:
        alias_dump = m_alias.model_dump(by_alias=True)
        field_dump = m_alias.model_dump()

    assert "someField" in alias_dump
    assert "some_field" in field_dump


def test_api_message_with_additional_field() -> None:
    class Msg(APIMessage):
        some_field: str

    m = Msg(detail="ok", someField="value")  # type: ignore[reportMissingParameter]
    assert m.detail == "ok"
    assert m.some_field == "value"

    if PYDANTIC_VERSION[0] == "2":
        dumped = m.model_dump(by_alias=True)
    else:
        dumped = m.model_dump(by_alias=True)

    assert dumped["someField"] == "value"
    assert dumped["detail"] == "ok"


def test_pydantic_v1_branch_reload(monkeypatch: MonkeyPatch) -> None:
    """Reload module with a fake pydantic.VERSION starting with '1' to hit the v1 else-branch."""
    import sys
    import importlib
    import pydantic as _pyd

    original_version = _pyd.VERSION
    try:
        monkeypatch.setattr(_pyd, "VERSION", ("1",))
        # ensure module is re-imported fresh
        sys.modules.pop("fastapi_utils.api_model", None)
        am = importlib.import_module("fastapi_utils.api_model")
        # the v1 path defines an inner `Config` class on APIModel
        assert hasattr(am.APIModel, "Config")
    finally:
        # restore original module state
        monkeypatch.setattr(_pyd, "VERSION", original_version)
        sys.modules.pop("fastapi_utils.api_model", None)
        importlib.import_module("fastapi_utils.api_model")
