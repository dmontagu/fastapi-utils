from __future__ import annotations

from enum import auto

from fastapi_utils.enums import CamelStrEnum, StrEnum


def test_str_enum() -> None:
    class MyStrEnum(StrEnum):
        choice_one = auto()
        choice_two = auto()

    values = [x.value for x in MyStrEnum]
    assert values == ["choice_one", "choice_two"]


def test_camel_str_enum() -> None:
    class MyCamelStrEnum(CamelStrEnum):
        choice_one = auto()
        choice_two = auto()

    values = [x.value for x in MyCamelStrEnum]
    assert values == ["choiceOne", "choiceTwo"]
