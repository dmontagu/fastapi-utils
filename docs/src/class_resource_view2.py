from fastapi import FastAPI

from docs.src.class_resource_view1 import MyApi
from fastapi_utils import Api


def create_app():
    app = FastAPI()
    api = Api(app)

    myapi = MyApi()
    api.add_resource(myapi, "/uri")

    return app


main = create_app()
