from enum import auto

from fastapi_utils.enums import StrEnum


class MyEnum(StrEnum):
    choice_a = auto()
    choice_b = auto()


assert MyEnum.choice_a.name == MyEnum.choice_a.value == "choice_a"
assert MyEnum.choice_b.name == MyEnum.choice_b.value == "choice_b"
