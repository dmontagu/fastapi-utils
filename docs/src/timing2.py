import asyncio
import logging

from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.testclient import TestClient

from fastapi_utils import timing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
timing.add_timing_middleware(
    app,
    record=logger.info,
    prefix="app",
    exclude="untimed",
    format_message=timing.json_formatter,
)
static_files_app = StaticFiles(directory=".")
app.mount(path="/static", app=static_files_app, name="static")


@app.get("/json/timed")
async def get_json_timed() -> None:
    await asyncio.sleep(0.05)


@app.get("/json/untimed")
async def get_json_untimed() -> None:
    await asyncio.sleep(0.1)


@app.get("/json/timed-intermediate")
async def get_json_with_intermediate_timing(request: Request) -> None:
    await asyncio.sleep(0.1)
    timing.record_timing(request, note="halfway")
    await asyncio.sleep(0.1)


TestClient(app).get("/json/timed")
# INFO:__main__:TIMING: {"wall_ms":53.0,"cpu_ms":1.2,"name":"app.__main__.get_json_timed","note":null}

TestClient(app).get("/json/untimed")
# <nothing logged>

TestClient(app).get("/json/timed-intermediate")
# INFO:__main__:TIMING: {"wall_ms":105.3,"cpu_ms":0.4,"name":"app.__main__.get_json_with_intermediate_timing","note":"halfway"}
# INFO:__main__:TIMING: {"wall_ms":206.7,"cpu_ms":1.1,"name":"app.__main__.get_json_timed","note":null}

TestClient(app).get("/static/test")
# INFO:__main__:TIMING: {"wall_ms":1.6,"cpu_ms":1.6,"name":"StaticFiles<'static'>","note":null}
