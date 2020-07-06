
from fastapi import APIRouter, FastAPI

from fastapi_utils.cbv import _cbv, INCLUDE_INIT_PARAMS_KEY


class Resource:

    def __init__(self, include_init_parameters=False):
        setattr(type(self), INCLUDE_INIT_PARAMS_KEY, include_init_parameters)
        self.router = APIRouter()

    def __call__(self, *urls, **kwargs):
        _cbv(self.router, type(self), *urls, instance=self)
        return self.router


class Api:
    def __init__(self, app: FastAPI):
        self.app = app

    def add_resource(self, resource: Resource, *urls, **kwargs):
        router = resource(*urls, **kwargs)
        self.app.include_router(router)
