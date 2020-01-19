from functools import partial

from pydantic import BaseConfig, BaseModel

from fastapi_utils.camelcase import snake2camel


class APIModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = partial(snake2camel, start_lower=True)


class APIMessage(APIModel):
    detail: str
