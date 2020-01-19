from fastapi import FastAPI

app = FastAPI()


@app.get("/resource")
def get_resource(resource_id: int) -> str:
    # the response will be serialized as a JSON number, *not* a string
    return resource_id
