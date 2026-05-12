"""Regression tests for issue #373.

The tasks module must use ``inspect.iscoroutinefunction`` rather than
``asyncio.iscoroutinefunction``, which is deprecated in Python 3.14
(``DeprecationWarning``) and scheduled for removal.

See: https://github.com/fastapiutils/fastapi-utils/issues/373
"""

from __future__ import annotations

import inspect

from fastapi_utils import tasks as tasks_module


def test_tasks_module_uses_inspect_iscoroutinefunction() -> None:
    source = inspect.getsource(tasks_module)
    assert "asyncio.iscoroutinefunction" not in source
    assert "inspect.iscoroutinefunction" in source
