import inspect
from abc import ABC

from fastapi import APIRouter, FastAPI

from fastapi_utils.cbv import _cbv


class Resource:
    def __init__(self):
        self.router = APIRouter()

    def __call__(self, *urls, **kwargs):
        _cbv(self.router, type(self), *urls)
        return self.router


class Api:
    def __init__(self, app: FastAPI):
        self.app = app

    def add_resource(self, resource: Resource, *urls, **kwargs):
        router = resource(*urls, **kwargs)
        self.app.include_router(router)
