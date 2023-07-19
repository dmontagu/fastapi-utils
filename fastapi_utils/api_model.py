from __future__ import annotations

from functools import partial

from pydantic import BaseModel
from pydantic import __version__ as pydantic_version

from fastapi_utils.camelcase import snake2camel

if pydantic_version < "2.0":
    from pydantic import BaseConfig
else:
    from pydantic import ConfigDict


class APIModel(BaseModel):
    """
    Intended for use as a base class for externally-facing models.

    Any models that inherit from this class will:
    * accept fields using snake_case or camelCase keys
    * use camelCase keys in the generated OpenAPI spec
    * have from_attributes on by default
        * Because of this, FastAPI will automatically attempt to parse returned orm instances into the model
    """

    if pydantic_version < "2.0":

        class Config(BaseConfig):
            orm_mode = True
            allow_population_by_field_name = True
            alias_generator = partial(snake2camel, start_lower=True)

    else:
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
