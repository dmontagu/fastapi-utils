from fastapi_utils import Resource


class MyApi(Resource):
    def get(self):
        return "done"
