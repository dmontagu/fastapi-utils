from fastapi_restful import Resource


class MyApi(Resource):
    def get(self):
        return "done"
