from enum import auto

from fastapi_utils.enums import CamelStrEnum


class MyEnum(CamelStrEnum):
    choice_a = auto()
    choice_b = auto()


assert MyEnum.choice_a.name == MyEnum.choice_a.value == "choiceOne"
assert MyEnum.choice_b.name == MyEnum.choice_b.value == "choiceTwo"
