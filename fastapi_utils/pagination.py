from __future__ import annotations

from functools import partial
from typing import Generic, List, Optional, Sequence, TypeVar

import pydantic
from fastapi import Query
from pydantic import Field

from .api_model import APIModel
from .camelcase import snake2camel

PYDANTIC_VERSION = pydantic.VERSION

DEFAULT_LIMIT = 50
MAX_LIMIT = 100

T = TypeVar("T")


class LimitOffsetParams:
    """
    A reusable FastAPI dependency for limit/offset pagination query parameters.
    """

    def __init__(
        self,
        limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
        offset: int = Query(0, ge=0),
    ):
        if not isinstance(limit, int):
            limit = DEFAULT_LIMIT
        if not isinstance(offset, int):
            offset = 0
        self._validate(limit=limit, offset=offset)
        self.limit = limit
        self.offset = offset

    @staticmethod
    def _validate(*, limit: int, offset: int) -> None:
        if limit < 1:
            raise ValueError("limit must be greater than or equal to 1")
        if limit > MAX_LIMIT:
            raise ValueError(f"limit must be less than or equal to {MAX_LIMIT}")
        if offset < 0:
            raise ValueError("offset must be greater than or equal to 0")


if PYDANTIC_VERSION[0] == "2":

    class _PageBase(APIModel):
        pass

else:
    from pydantic.generics import GenericModel

    class _PageBase(GenericModel):
        class Config:
            orm_mode = True
            allow_population_by_field_name = True
            alias_generator = partial(snake2camel, start_lower=True)


class Page(_PageBase, Generic[T]):
    """
    A generic response model for limit/offset paginated endpoints.
    """

    items: List[T]
    total: int = Field(..., ge=0)
    limit: int = Field(..., ge=1)
    offset: int = Field(..., ge=0)
    next_offset: Optional[int] = Field(None, ge=0)
    previous_offset: Optional[int] = Field(None, ge=0)


def paginate(items: Sequence[T], *, total: int, params: LimitOffsetParams) -> Page[T]:
    """
    Builds a paginated response from an already-paginated sequence and total count.
    """
    if total < 0:
        raise ValueError("total must be greater than or equal to 0")

    next_offset = params.offset + params.limit
    if next_offset >= total:
        next_offset = None

    previous_offset = None
    if params.offset > 0:
        previous_offset = max(params.offset - params.limit, 0)

    return Page(
        items=list(items),
        total=total,
        limit=params.limit,
        offset=params.offset,
        next_offset=next_offset,
        previous_offset=previous_offset,
    )
