from fastapi import FastAPI
from fastapi_restful import Api

from docs.src.class_resource_view1 import MyApi


def main():
    app = FastAPI()
    api = Api(app)

    myapi = MyApi()
    api.add_resource(myapi, "/uri")


if __name__ == "__main__":
    main()
