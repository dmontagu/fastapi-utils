import asyncio
import logging

from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.testclient import TestClient

from fastapi_utils.timing import add_timing_middleware, record_timing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
add_timing_middleware(app, record=logger.info, prefix="app", exclude="untimed")
static_files_app = StaticFiles(directory=".")
app.mount(path="/static", app=static_files_app, name="static")


@app.get("/timed")
async def get_timed() -> None:
    await asyncio.sleep(0.05)


@app.get("/untimed")
async def get_untimed() -> None:
    await asyncio.sleep(0.1)


@app.get("/timed-intermediate")
async def get_with_intermediate_timing(request: Request) -> None:
    await asyncio.sleep(0.1)
    record_timing(request, note="halfway")
    await asyncio.sleep(0.1)


TestClient(app).get("/timed")
# INFO:__main__:TIMING: Wall:   53.0ms
#   | CPU:    1.2ms
#   | app.__main__.get_timed

TestClient(app).get("/untimed")
# <nothing logged>

TestClient(app).get("/timed-intermediate")
# INFO:__main__:TIMING: Wall:  105.3ms
#   | CPU:    0.4ms
#   | app.__main__.get_with_intermediate_timing (halfway)
# INFO:__main__:TIMING: Wall:  206.7ms
#   | CPU:    1.1ms
#   | app.__main__.get_with_intermediate_timing

TestClient(app).get("/static/test")
# INFO:__main__:TIMING: Wall:    1.6ms
#   | CPU:    1.6ms
#   | StaticFiles<'static'>
