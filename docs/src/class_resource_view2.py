from fastapi import FastAPI

from docs.src.class_resource_view1 import MyApi
from fastapi_restful import Api


def main():
    app = FastAPI()
    api = Api(app)

    myapi = MyApi()
    api.add_resource(myapi, "/uri")


if __name__ == "__main__":
    main()
