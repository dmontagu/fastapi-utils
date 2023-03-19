from __future__ import annotations

from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.testclient import TestClient

from fastapi_utils.timing import add_timing_middleware, record_timing

app = FastAPI()
add_timing_middleware(app, exclude="untimed")
static_files_app = StaticFiles(directory=".")
app.mount(path="/static", app=static_files_app, name="static")


@app.get("/timed")
def get_timed() -> None:
    pass


@app.get("/untimed")
def get_untimed() -> None:
    pass


client = TestClient(app)


def test_timing(capsys: CaptureFixture[str]) -> None:
    client.get("/timed")
    out, err = capsys.readouterr()
    assert err == ""
    assert out.startswith("TIMING: Wall")
    assert "CPU:" in out
    assert out.endswith("test_timing.get_timed\n")


def test_silent_timing(capsys: CaptureFixture[str]) -> None:
    client.get("/untimed")
    out, err = capsys.readouterr()
    assert err == ""
    assert out == ""


def test_mount(capsys: CaptureFixture[str]) -> None:
    basename = Path(__file__).name
    client.get(f"/static/{basename}")
    out, err = capsys.readouterr()
    assert err == ""
    assert out.startswith("TIMING:")
    assert out.endswith("StaticFiles<'static'>\n")


def test_missing(capsys: CaptureFixture[str]) -> None:
    client.get("/will-404")
    out, err = capsys.readouterr()
    assert err == ""
    assert out.startswith("TIMING:")
    assert out.endswith("<Path: /will-404>\n")


app2 = FastAPI()
add_timing_middleware(app2, prefix="app2")


@app2.get("/")
def get_with_intermediate_timing(request: Request) -> None:
    record_timing(request, note="hello")


client2 = TestClient(app2)


def test_intermediate(capsys: CaptureFixture[str]) -> None:
    client2.get("/")
    out, err = capsys.readouterr()
    assert err == ""
    outs = out.strip().split("\n")
    assert len(outs) == 2
    assert outs[0].startswith("TIMING:")
    assert outs[0].endswith("test_timing.get_with_intermediate_timing (hello)")
    assert outs[1].startswith("TIMING:")
    assert outs[1].endswith("test_timing.get_with_intermediate_timing")


app3 = FastAPI()


@app3.get("/")
def fail_to_record(request: Request) -> None:
    record_timing(request)


client3 = TestClient(app3)


def test_recording_fails_without_middleware() -> None:
    with pytest.raises(ValueError) as exc_info:
        client3.get("/")
    assert str(exc_info.value) == "No timer present on request"
