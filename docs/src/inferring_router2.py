from fastapi import FastAPI

from fastapi_utils.inferring_router import InferringRouter

app = FastAPI()


@app.get("/default")
def get_resource(resource_id: int) -> str:
    # the response will be serialized as a JSON number, *not* a string
    return resource_id


router = InferringRouter()


@router.get("/inferred")
def get_resource(resource_id: int) -> str:
    # thanks to InferringRouter, the response will be serialized as a string
    return resource_id


app.include_router(router)


def get_response_schema(openapi_spec, endpoint_path):
    responses = openapi_spec["paths"][endpoint_path]["get"]["responses"]
    return responses["200"]["content"]["application/json"]["schema"]


openapi_spec = app.openapi()
assert get_response_schema(openapi_spec, "/default") == {}
assert get_response_schema(openapi_spec, "/inferred")["type"] == "string"
