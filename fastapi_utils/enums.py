from enum import Enum

from fastapi_utils.camelcase import snake2camel


class StrEnum(str, Enum):
    """
    StrEnum subclasses that create variants using `auto()` will have values equal to their names
    Enums inheriting from this class that set values using `enum.auto()` will have variant values equal to their names
    """

    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values) -> str:  # type: ignore
        """
        Uses the name as the automatic value, rather than an integer

        See https://docs.python.org/3/library/enum.html#using-automatic-values for reference
        """
        return name


class CamelStrEnum(str, Enum):
    """
    CamelStrEnum subclasses that create variants using `auto()` will have values equal to their camelCase names
    """

    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values) -> str:  # type: ignore
        """
        Uses the camelCase name as the automatic value, rather than an integer

        See https://docs.python.org/3/library/enum.html#using-automatic-values for reference
        """
        return snake2camel(name, start_lower=True)
