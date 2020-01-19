"""
Based on https://github.com/steinnes/timing-asgi.git
"""
import resource
import time
from typing import Any, Callable, Optional

from fastapi import FastAPI
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match, Mount


class TimingStats:
    def __init__(
        self, name: Optional[str] = None, record: Callable[[str], None] = None, exclude: Optional[str] = None
    ) -> None:
        self.name = name
        self.record = record or print

        self.start_time: float = 0
        self.start_cpu_time: float = 0
        self.end_cpu_time: float = 0
        self.end_time: float = 0
        self.silent: bool = False

        if self.name and exclude and (exclude in self.name):
            self.silent = True

    def start(self) -> None:
        self.start_time = time.time()
        self.start_cpu_time = get_cpu_time()

    def take_split(self) -> None:
        self.end_time = time.time()
        self.end_cpu_time = get_cpu_time()

    @property
    def time(self) -> float:
        return self.end_time - self.start_time

    @property
    def cpu_time(self) -> float:
        return self.end_cpu_time - self.start_cpu_time

    def __enter__(self) -> "TimingStats":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.emit()

    def emit(self, note: Optional[str] = None) -> None:
        if not self.silent:
            self.take_split()
            cpu_ms = 1000 * self.cpu_time
            wall_ms = 1000 * self.time
            message = f"TIMING: Wall: {wall_ms:6.1f}ms | CPU: {cpu_ms:6.1f}ms | {self.name}"
            if note is not None:
                message += f" ({note})"
            self.record(message)


class MetricNamer:
    def __init__(self, prefix: str, app: FastAPI):
        if prefix:
            prefix += "."
        self.prefix = prefix
        self.app = app

    def __call__(self, scope: Any) -> str:
        route = None
        for r in self.app.router.routes:
            if r.matches(scope)[0] == Match.FULL:
                route = r
                break
        if hasattr(route, "endpoint") and hasattr(route, "name"):
            name = f"{self.prefix}{route.endpoint.__module__}.{route.name}"  # type: ignore
        elif isinstance(route, Mount):
            name = f"{type(route.app).__name__}<{route.name!r}>"
        else:
            name = str(f"<Path: {scope['path']}>")
        return name


def get_cpu_time() -> float:
    # taken from timing-asgi
    resources = resource.getrusage(resource.RUSAGE_SELF)
    # add up user time (ru_utime) and system time (ru_stime)
    return resources[0] + resources[1]


def add_timing_middleware(
    app: FastAPI, record: Callable[[str], None] = None, prefix: str = "", exclude: Optional[str] = None
) -> None:
    """
    Don't print timings if exclude occurs as an exact substring of the generated metric name
    """
    metric_namer = MetricNamer(prefix=prefix, app=app)

    @app.middleware("http")
    async def timing_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
        metric_name = metric_namer(request.scope)
        with TimingStats(metric_name, record=record, exclude=exclude) as timer:
            request.state.timer = timer
            response = await call_next(request)
        return response


def record_timing(request: Request, note: Optional[str] = None) -> None:
    """
    Call this function anywhere you want to display performance information while handling a single request
    """
    if hasattr(request.state, "timer"):
        assert isinstance(request.state.timer, TimingStats)
        request.state.timer.emit(note)
    else:
        print("TIMING ERROR: No timer present on request")
