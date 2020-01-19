from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/resource/{resource_id}")
def get_resource(resource_id: int) -> int:
    return resource_id


operation_id = app.openapi()["paths"]["/api/v1/resource/{resource_id}"]["get"]["operationId"]
assert operation_id == "get_resource_api_v1_resource__resource_id__get"
