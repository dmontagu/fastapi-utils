from pydantic import BaseModel

from fastapi_utils import Resource, set_responses


# Setup
class ResponseModel(BaseModel):
    answer: str


class NotFoundModel(BaseModel):
    IsFound: bool

# Setup end


class MyApi(Resource):
    def __init__(self, mongo_client):
        self.mongo = mongo_client

    @set_responses(ResponseModel)
    def get(self):
        return 'done'

    @set_responses(ResponseModel, 201, {404: NotFoundModel})
    def post(self):
        return 'Done again'
