import asyncio
import sys
from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    if sys.version_info >= (3, 8):
        from unittest.mock import AsyncMock, call, patch
    else:
        from mock import AsyncMock, call, patch
else:
    try:
        from unittest.mock import AsyncMock, call, patch
    except ImportError:
        from mock import AsyncMock, call, patch

import pytest

from fastapi_utils.tasks import NoArgsNoReturnAsyncFuncT, repeat_every


# Fixtures:
@pytest.fixture(scope="module")
def seconds() -> float:
    return 0.01


@pytest.fixture(scope="module")
def max_repetitions() -> int:
    return 3


@pytest.fixture(scope="module")
def wait_first(seconds: float) -> float:
    return seconds


# Tests:
class TestRepeatEveryBase:
    def setup_method(self) -> None:
        self.counter = 0
        self.completed = asyncio.Event()

    def increase_counter(self) -> None:
        self.counter += 1

    async def increase_counter_async(self) -> None:
        self.increase_counter()

    def loop_completed(self) -> None:
        self.completed.set()

    async def loop_completed_async(self) -> None:
        self.loop_completed()

    def kill_loop(self, exc: Exception) -> None:
        self.completed.set()
        raise exc

    async def kill_loop_async(self, exc: Exception) -> None:
        self.kill_loop(exc)

    def continue_loop(self, exc: Exception) -> None:
        return

    async def continue_loop_async(self, exc: Exception) -> None:
        self.continue_loop(exc)

    def raise_exc(self) -> NoReturn:
        self.increase_counter()
        raise ValueError("error")

    async def raise_exc_async(self) -> NoReturn:
        self.raise_exc()

    @pytest.fixture
    def increase_counter_task(self, is_async: bool, seconds: float, max_repetitions: int) -> NoArgsNoReturnAsyncFuncT:
        decorator = repeat_every(seconds=seconds, max_repetitions=max_repetitions, on_complete=self.loop_completed)
        if is_async:
            return decorator(self.increase_counter_async)
        else:
            return decorator(self.increase_counter)

    @pytest.fixture
    def wait_first_increase_counter_task(
        self, is_async: bool, seconds: float, max_repetitions: int, wait_first: float
    ) -> NoArgsNoReturnAsyncFuncT:
        decorator = repeat_every(
            seconds=seconds, max_repetitions=max_repetitions, wait_first=wait_first, on_complete=self.loop_completed
        )
        if is_async:
            return decorator(self.increase_counter_async)
        else:
            return decorator(self.increase_counter)

    @pytest.fixture
    def stop_on_exception_task(self, is_async: bool, seconds: float, max_repetitions: int) -> NoArgsNoReturnAsyncFuncT:
        if is_async:
            decorator = repeat_every(
                seconds=seconds,
                max_repetitions=max_repetitions,
                on_complete=self.loop_completed_async,
                on_exception=self.kill_loop_async,
            )
            return decorator(self.raise_exc_async)
        else:
            decorator = repeat_every(
                seconds=seconds,
                max_repetitions=max_repetitions,
                on_complete=self.loop_completed,
                on_exception=self.kill_loop,
            )
            return decorator(self.raise_exc)

    @pytest.fixture
    def suppressed_exception_task(
        self, is_async: bool, seconds: float, max_repetitions: int
    ) -> NoArgsNoReturnAsyncFuncT:
        if is_async:
            decorator = repeat_every(
                seconds=seconds,
                max_repetitions=max_repetitions,
                on_complete=self.loop_completed_async,
                on_exception=self.continue_loop_async,
            )
            return decorator(self.raise_exc_async)
        else:
            decorator = repeat_every(
                seconds=seconds,
                max_repetitions=max_repetitions,
                on_complete=self.loop_completed,
                on_exception=self.continue_loop,
            )
            return decorator(self.raise_exc)


class TestRepeatEveryWithSynchronousFunction(TestRepeatEveryBase):
    @pytest.fixture
    def is_async(self) -> bool:
        return False

    @pytest.mark.asyncio
    @pytest.mark.timeout(1)
    @patch("asyncio.sleep")
    async def test_max_repetitions(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        increase_counter_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await increase_counter_task()
        await self.completed.wait()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls(max_repetitions * [call(seconds)], any_order=True)

    @pytest.mark.asyncio
    @pytest.mark.timeout(1)
    @patch("asyncio.sleep")
    async def test_max_repetitions_and_wait_first(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        wait_first_increase_counter_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await wait_first_increase_counter_task()
        await self.completed.wait()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls((max_repetitions + 1) * [call(seconds)], any_order=True)

    @pytest.mark.asyncio
    @pytest.mark.timeout(1)
    async def test_stop_loop_on_exc(
        self,
        stop_on_exception_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await stop_on_exception_task()
        await self.completed.wait()

        assert self.counter == 1

    @pytest.mark.asyncio
    @pytest.mark.timeout(1)
    @patch("asyncio.sleep")
    async def test_continue_loop_on_exc(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        suppressed_exception_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await suppressed_exception_task()
        await self.completed.wait()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls(max_repetitions * [call(seconds)], any_order=True)


class TestRepeatEveryWithAsynchronousFunction(TestRepeatEveryBase):
    @pytest.fixture
    def is_async(self) -> bool:
        return True

    @pytest.mark.asyncio
    @pytest.mark.timeout(1)
    @patch("asyncio.sleep")
    async def test_max_repetitions(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        increase_counter_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await increase_counter_task()
        await self.completed.wait()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls(max_repetitions * [call(seconds)], any_order=True)

    @pytest.mark.asyncio
    @pytest.mark.timeout(1)
    @patch("asyncio.sleep")
    async def test_max_repetitions_and_wait_first(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        wait_first_increase_counter_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await wait_first_increase_counter_task()
        await self.completed.wait()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls((max_repetitions + 1) * [call(seconds)], any_order=True)

    @pytest.mark.asyncio
    @pytest.mark.timeout(1)
    async def test_stop_loop_on_exc(
        self,
        stop_on_exception_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await stop_on_exception_task()
        await self.completed.wait()

        assert self.counter == 1

    @pytest.mark.asyncio
    @pytest.mark.timeout(1)
    @patch("asyncio.sleep")
    async def test_continue_loop_on_exc(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        suppressed_exception_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await suppressed_exception_task()
        await self.completed.wait()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls(max_repetitions * [call(seconds)], any_order=True)
