from __future__ import annotations

from enum import auto

from fastapi_restful.enums import CamelStrEnum, StrEnum


class TestEnums:
    def test_str_enum(self) -> None:
        class MyStrEnum(StrEnum):
            choice_one = auto()
            choice_two = auto()

        values = [value for value in MyStrEnum]
        assert values == ["choice_one", "choice_two"]

    def test_camelcase_str_conversion(self) -> None:
        class MyCamelStrEnum(CamelStrEnum):
            choice_one = auto()
            choice_two = auto()

        values = [value for value in MyCamelStrEnum]
        assert values == ["choiceOne", "choiceTwo"]
