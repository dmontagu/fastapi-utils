from typing import Any

from fastapi import APIRouter, FastAPI

from fastapi_utils.cbv import INCLUDE_INIT_PARAMS_KEY, RESOURCE_CLASS_KEY, _cbv


class Resource:
    def __init__(self, include_init_parameters: bool = False) -> None:
        setattr(type(self), RESOURCE_CLASS_KEY, True)
        setattr(type(self), INCLUDE_INIT_PARAMS_KEY, include_init_parameters)
        self.router = APIRouter()

    def __call__(self, *urls: str, **kwargs: Any) -> APIRouter:
        _cbv(self.router, type(self), *urls)
        return self.router


class Api:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def add_resource(self, resource: Resource, *urls: str, **kwargs: Any) -> None:
        router = resource(*urls, **kwargs)
        self.app.include_router(router)
