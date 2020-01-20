from fastapi import FastAPI

app = FastAPI()


@app.get("/default")
def get_resource(resource_id: int) -> str:
    # the response will be serialized as a JSON number, *not* a string
    return resource_id


def get_response_schema(openapi_spec, endpoint_path):
    responses = openapi_spec["paths"][endpoint_path]["get"]["responses"]
    return responses["200"]["content"]["application/json"]["schema"]


openapi_spec = app.openapi()
assert get_response_schema(openapi_spec, "/default") == {}
