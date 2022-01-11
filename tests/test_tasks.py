import asyncio
import logging
import time
from asyncio import AbstractEventLoop
from typing import TYPE_CHECKING, Any, Dict, List, NoReturn, Tuple

import pytest
from pytest import LogCaptureFixture

if TYPE_CHECKING:
    from pytest.capture import CaptureFixture
else:
    CaptureFixture = Any

from fastapi_restful.tasks import repeat_every

logging.basicConfig(level=logging.INFO)


def ignore_exception(_loop: AbstractEventLoop, _context: Dict[str, Any]) -> None:
    pass


@pytest.fixture(autouse=True)
def setup_event_loop(event_loop: AbstractEventLoop) -> None:
    event_loop.set_exception_handler(ignore_exception)


@pytest.mark.asyncio
async def test_repeat_print(capsys: CaptureFixture) -> None:
    @repeat_every(seconds=0.01, max_repetitions=3)
    async def repeatedly_print_hello() -> None:
        print("hello")

    await repeatedly_print_hello()
    await asyncio.sleep(0.1)
    out, err = capsys.readouterr()
    assert out == "hello\n" * 3
    assert err == ""


@pytest.mark.asyncio
async def test_repeat_print_delay(capsys: CaptureFixture) -> None:
    @repeat_every(seconds=0.07, max_repetitions=3)
    def repeatedly_print_hello() -> None:
        print("hello")

    await repeatedly_print_hello()
    await asyncio.sleep(0.1)
    out, err = capsys.readouterr()
    assert out == "hello\n" * 2
    assert err == ""


@pytest.mark.asyncio
async def test_repeat_print_wait(capsys: CaptureFixture) -> None:
    @repeat_every(seconds=0.07, max_repetitions=3, wait_first=0.1)
    async def repeatedly_print_hello() -> None:
        print("hello")

    await repeatedly_print_hello()
    await asyncio.sleep(0.15)
    out, err = capsys.readouterr()
    assert out == "hello\n" * 1
    assert err == ""


@pytest.mark.asyncio
async def test_repeat_unlogged_error(caplog: LogCaptureFixture) -> None:
    @repeat_every(seconds=0.07, max_repetitions=None)
    def log_exc() -> NoReturn:
        raise ValueError("repeat")

    await log_exc()
    await asyncio.sleep(0.1)
    record_tuples = [x for x in caplog.record_tuples if x[0] == __name__]
    print(caplog.record_tuples)
    assert len(record_tuples) == 0


@pytest.mark.asyncio
async def test_repeat_log_error(caplog: LogCaptureFixture) -> None:
    logger = logging.getLogger(__name__)

    @repeat_every(seconds=0.1, max_repetitions=None, logger=logger)
    def log_exc() -> NoReturn:
        raise ValueError("repeat")

    await log_exc()
    n_record_tuples = 0
    record_tuples: List[Tuple[Any, ...]] = []
    start_time = time.time()
    while n_record_tuples < 2:  # ensure multiple records are logged
        time_elapsed = time.time() - start_time
        if time_elapsed > 1:
            print(record_tuples)
            assert False, "Test timed out"
        await asyncio.sleep(0.05)
        record_tuples = [x for x in caplog.record_tuples if x[0] == __name__]
        n_record_tuples = len(record_tuples)


@pytest.mark.asyncio
async def test_repeat_raise_error(caplog: LogCaptureFixture, capsys: CaptureFixture) -> None:
    logger = logging.getLogger(__name__)

    @repeat_every(seconds=0.07, max_repetitions=None, raise_exceptions=True, logger=logger)
    def raise_exc() -> NoReturn:
        raise ValueError("repeat")

    await raise_exc()
    await asyncio.sleep(0.1)
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""
    record_tuples = [x for x in caplog.record_tuples if x[0] == __name__]
    print(caplog.record_tuples)
    assert len(record_tuples) == 1
