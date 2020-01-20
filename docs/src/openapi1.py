from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/resource/{resource_id}")
def get_resource(resource_id: int) -> int:
    return resource_id


path_spec = app.openapi()["paths"]["/api/v1/resource/{resource_id}"]
operation_id = path_spec["get"]["operationId"]
assert operation_id == "get_resource_api_v1_resource__resource_id__get"
