from fastapi import FastAPI

from fastapi_utils.inferring_router import InferringRouter

app = FastAPI()


@app.get("/resource")
def get_resource(resource_id: int) -> str:
    # the response will be serialized as a JSON number, *not* a string
    return resource_id


router = InferringRouter()


@router.get("/inferred-resource")
def get_resource(resource_id: int) -> str:
    # thanks to InferringRouter, the response *will* be serialized as a JSON string
    return resource_id


app.include_router(router)
openapi_paths = app.openapi()["paths"]
resource_response_schema = (
    openapi_paths["/resource"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
)
assert resource_response_schema == {}

inferred_resource_response_schema = (
    openapi_paths["/inferred-resource"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
)
assert inferred_resource_response_schema["type"] == "string"
