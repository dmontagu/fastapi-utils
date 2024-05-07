from pydantic import BaseModel

from fastapi_utils import Resource, set_responses


# Setup
class ResponseModel(BaseModel):
    answer: str


class ResourceAlreadyExistsModel(BaseModel):
    is_found: bool


class ResourceModel(BaseModel):
    ID: str
    name: str


# Setup end


class MyApi(Resource):
    def __init__(self, mongo_client):
        self.mongo = mongo_client

    @set_responses(ResponseModel)
    def get(self):
        return "Done"

    @set_responses(ResponseModel, 200)
    def put(self):
        return "Redone"

    @set_responses(
        ResponseModel,
        201,
        {
            409: {
                "description": "The path can't be found",
                "model": ResourceAlreadyExistsModel,
            }
        },
    )
    def post(self, res: ResourceModel):
        if self.mongo.is_resource_exist(res.name):
            return JSONResponse(409, content={"is_found": true})
        return "Done again"
