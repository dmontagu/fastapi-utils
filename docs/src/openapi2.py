from fastapi import FastAPI

from fastapi_utils.openapi import simplify_operation_ids

app = FastAPI()


@app.get("/api/v1/resource/{resource_id}")
def get_resource(resource_id: int) -> int:
    return resource_id


simplify_operation_ids(app)

operation_id = app.openapi()["paths"]["/api/v1/resource/{resource_id}"]["get"]["operationId"]
assert operation_id == "get_resource"
