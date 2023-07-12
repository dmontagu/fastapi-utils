from __future__ import annotations

from functools import partial

from pydantic import BaseModel, ConfigDict

from fastapi_utils.camelcase import snake2camel


class APIModel(BaseModel):
    """
    Intended for use as a base class for externally-facing models.

    Any models that inherit from this class will:
    * accept fields using snake_case or camelCase keys
    * use camelCase keys in the generated OpenAPI spec
    * have from_attributes on by default
        * Because of this, FastAPI will automatically attempt to parse returned orm instances into the model
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=partial(snake2camel, start_lower=True),
    )


class APIMessage(APIModel):
    """
    A lightweight utility class intended for use with simple message-returning endpoints.
    """

    detail: str
