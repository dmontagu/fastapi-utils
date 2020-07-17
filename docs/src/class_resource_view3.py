from fastapi import FastAPI
from fastapi_restful import Api
from pymongo import MongoClient

from docs.src.class_resource_view1 import MyApi


def main():
    app = FastAPI()
    api = Api(app)

    mongo_client = MongoClient("mongodb://localhost:27017")
    myapi = MyApi(mongo_client)
    api.add_resource(myapi, "/uri")


if __name__ == "__main__":
    main()
