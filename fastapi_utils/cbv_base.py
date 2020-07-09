from functools import partial, wraps
from fastapi import APIRouter, FastAPI

from fastapi_utils.cbv import _cbv, INCLUDE_INIT_PARAMS_KEY, RETURN_TYPES_FUNC_KEY


class Resource:
    # raise NotImplementedError
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


def set_responses(response, status_code=200, responses=None):
    def decorator(func):

        def get_responses():
            return response, status_code, responses

        setattr(func, RETURN_TYPES_FUNC_KEY, get_responses)
        return func
    return decorator
