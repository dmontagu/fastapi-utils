
from fastapi import APIRouter, FastAPI

from fastapi_utils.cbv import _cbv, INCLUDE_INIT_PARAMS_KEY


class Resource:
    pass


class Api:
    def __init__(self, app: FastAPI):
        self.app = app

    def add_resource(self, resource: Resource, *urls, **kwargs):
        router = APIRouter()
        _cbv(router, type(resource), *urls, instance=resource)
        self.app.include_router(router)


def take_init_parameters(cls):
    setattr(cls, INCLUDE_INIT_PARAMS_KEY, True)
    return cls
