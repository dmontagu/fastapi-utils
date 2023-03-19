from __future__ import annotations

import pytest

from fastapi_utils.camelcase import camel2snake, snake2camel


@pytest.mark.parametrize(
    "value,result",
    [
        ("snake_to_camel", "snakeToCamel"),
        ("snake_2_camel", "snake2Camel"),
        ("snake2camel", "snake2Camel"),
        ("_snake_to_camel", "_snakeToCamel"),
        ("snake_to_camel_", "snakeToCamel_"),
        ("__snake_to_camel__", "__snakeToCamel__"),
        ("snake_2", "snake2"),
        ("_snake_2", "_snake2"),
        ("snake_2_", "snake2_"),
    ],
)
def test_snake2camel_start_lower(value: str, result: str) -> None:
    assert snake2camel(value, start_lower=True) == result


@pytest.mark.parametrize(
    "value,result",
    [
        ("snake_to_camel", "SnakeToCamel"),
        ("snake_2_camel", "Snake2Camel"),
        ("snake2camel", "Snake2Camel"),
        ("_snake_to_camel", "_SnakeToCamel"),
        ("snake_to_camel_", "SnakeToCamel_"),
        ("__snake_to_camel__", "__SnakeToCamel__"),
        ("snake_2", "Snake2"),
        ("_snake_2", "_Snake2"),
        ("snake_2_", "Snake2_"),
    ],
)
def test_snake2camel(value: str, result: str) -> None:
    assert snake2camel(value) == result


@pytest.mark.parametrize(
    "value,result",
    [
        ("camel_to_snake", "camel_to_snake"),
        ("camelToSnake", "camel_to_snake"),
        ("camel2Snake", "camel_2_snake"),
        ("_camelToSnake", "_camel_to_snake"),
        ("camelToSnake_", "camel_to_snake_"),
        ("__camelToSnake__", "__camel_to_snake__"),
        ("CamelToSnake", "camel_to_snake"),
        ("Camel2Snake", "camel_2_snake"),
        ("_CamelToSnake", "_camel_to_snake"),
        ("CamelToSnake_", "camel_to_snake_"),
        ("__CamelToSnake__", "__camel_to_snake__"),
        ("Camel2", "camel_2"),
        ("Camel2_", "camel_2_"),
        ("_Camel2", "_camel_2"),
        ("camel2", "camel_2"),
        ("camel2_", "camel_2_"),
        ("_camel2", "_camel_2"),
    ],
)
def test_camel2snake(value: str, result: str) -> None:
    assert camel2snake(value) == result
