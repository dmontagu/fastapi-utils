from fastapi import FastAPI
from pymongo import MongoClient

from docs.src.class_resource_view1 import MyApi
from fastapi_utils import Api


def create_app():
    app = FastAPI()
    api = Api(app)

    mongo_client = MongoClient("mongodb://localhost:27017")
    myapi = MyApi(mongo_client)
    api.add_resource(myapi, "/uri")

    return app


main = create_app()
