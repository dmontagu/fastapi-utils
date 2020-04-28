from enum import auto

from fastapi_utils.enums import CamelStrEnum


class MyEnum(CamelStrEnum):
    choice_one = auto()
    choice_two = auto()


assert MyEnum.choice_one.name == MyEnum.choice_one.value == "choiceOne"
assert MyEnum.choice_one.name == MyEnum.choice_one.value == "choiceTwo"
