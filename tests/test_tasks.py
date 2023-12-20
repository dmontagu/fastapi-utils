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

from fastapi_restful.tasks import NoArgsNoReturnAsyncFuncT, repeat_every


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

    def increase_counter(self) -> None:
        self.counter += 1


class TestRepeatEveryWithSynchronousFunction(TestRepeatEveryBase):
    @pytest.fixture
    def increase_counter_task(self, seconds: float, max_repetitions: int) -> NoArgsNoReturnAsyncFuncT:
        return repeat_every(seconds=seconds, max_repetitions=max_repetitions)(self.increase_counter)

    @pytest.fixture
    def wait_first_increase_counter_task(
        self, seconds: float, max_repetitions: int, wait_first: float
    ) -> NoArgsNoReturnAsyncFuncT:
        decorator = repeat_every(seconds=seconds, max_repetitions=max_repetitions, wait_first=wait_first)
        return decorator(self.increase_counter)

    @staticmethod
    @pytest.fixture
    def raising_task(seconds: float, max_repetitions: int) -> NoArgsNoReturnAsyncFuncT:
        @repeat_every(seconds=seconds, max_repetitions=max_repetitions)
        def raise_exc() -> NoReturn:
            raise ValueError("error")

        return raise_exc

    @staticmethod
    @pytest.fixture
    def suppressed_exception_task(seconds: float, max_repetitions: int) -> NoArgsNoReturnAsyncFuncT:
        @repeat_every(seconds=seconds, raise_exceptions=True)
        def raise_exc() -> NoReturn:
            raise ValueError("error")

        return raise_exc

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    async def test_max_repetitions(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        increase_counter_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await increase_counter_task()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls(max_repetitions * [call(seconds)], any_order=True)

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    async def test_max_repetitions_and_wait_first(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        wait_first: float,
        wait_first_increase_counter_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await wait_first_increase_counter_task()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls((max_repetitions + 1) * [call(seconds)], any_order=True)

    @pytest.mark.asyncio
    async def test_raise_exceptions_false(
        self, seconds: float, max_repetitions: int, raising_task: NoArgsNoReturnAsyncFuncT
    ) -> None:
        try:
            await raising_task()
        except ValueError as e:
            pytest.fail(f"{self.test_raise_exceptions_false.__name__} raised an exception: {e}")

    @pytest.mark.asyncio
    async def test_raise_exceptions_true(
        self, seconds: float, suppressed_exception_task: NoArgsNoReturnAsyncFuncT
    ) -> None:
        with pytest.raises(ValueError):
            await suppressed_exception_task()


class TestRepeatEveryWithAsynchronousFunction(TestRepeatEveryBase):
    @pytest.fixture
    def increase_counter_task(self, seconds: float, max_repetitions: int) -> NoArgsNoReturnAsyncFuncT:
        return repeat_every(seconds=seconds, max_repetitions=max_repetitions)(self.increase_counter)

    @pytest.fixture
    def wait_first_increase_counter_task(
        self, seconds: float, max_repetitions: int, wait_first: float
    ) -> NoArgsNoReturnAsyncFuncT:
        decorator = repeat_every(seconds=seconds, max_repetitions=max_repetitions, wait_first=wait_first)
        return decorator(self.increase_counter)

    @staticmethod
    @pytest.fixture
    def raising_task(seconds: float, max_repetitions: int) -> NoArgsNoReturnAsyncFuncT:
        @repeat_every(seconds=seconds, max_repetitions=max_repetitions)
        async def raise_exc() -> NoReturn:
            raise ValueError("error")

        return raise_exc

    @staticmethod
    @pytest.fixture
    def suppressed_exception_task(seconds: float, max_repetitions: int) -> NoArgsNoReturnAsyncFuncT:
        @repeat_every(seconds=seconds, raise_exceptions=True)
        async def raise_exc() -> NoReturn:
            raise ValueError("error")

        return raise_exc

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    async def test_max_repetitions(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        increase_counter_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await increase_counter_task()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls(max_repetitions * [call(seconds)], any_order=True)

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    async def test_max_repetitions_and_wait_first(
        self,
        asyncio_sleep_mock: AsyncMock,
        seconds: float,
        max_repetitions: int,
        wait_first_increase_counter_task: NoArgsNoReturnAsyncFuncT,
    ) -> None:
        await wait_first_increase_counter_task()

        assert self.counter == max_repetitions
        asyncio_sleep_mock.assert_has_calls((max_repetitions + 1) * [call(seconds)], any_order=True)

    @pytest.mark.asyncio
    async def test_raise_exceptions_false(
        self, seconds: float, max_repetitions: int, raising_task: NoArgsNoReturnAsyncFuncT
    ) -> None:
        try:
            await raising_task()
        except ValueError as e:
            pytest.fail(f"{self.test_raise_exceptions_false.__name__} raised an exception: {e}")

    @pytest.mark.asyncio
    async def test_raise_exceptions_true(
        self, seconds: float, suppressed_exception_task: NoArgsNoReturnAsyncFuncT
    ) -> None:
        with pytest.raises(ValueError):
            await suppressed_exception_task()
