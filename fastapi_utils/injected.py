
from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any, NoReturn, TypeVar, overload

from fastapi import Depends, FastAPI
from fastapi.dependencies.models import Dependant
from fastapi.routing import APIRoute

_AnyType = TypeVar("_AnyType")


class _DependsPlaceholder:
    """A placeholder for dependencies that will be bound in main.py / conftest.py
    because FastAPI greedily resolves dependencies when routes are added.

    It compares/hashes as the type it wraps so that FastAPI.dependency_overrides works.

    The idea is that we can bind dependencies in main.py / conftest.py and then
    check that every dependency was bound before starting the app so that we fail
    at startup instead of at runtime or import time.
    """

    def __init__(self, t: Any) -> None:
        self.t = t

    def __eq__(self, __value: object) -> bool:
        return __value == self.t

    def __hash__(self) -> int:
        return hash(self.t)

    async def __call__(self) -> NoReturn:  # pragma: no cover
        raise RuntimeError(
            f"No dependency override found for {self.t}."
            " Did you add it to app.dependency_overrides in main.create_app?"
        )


class InjectedTracker:
    def __class_getitem__(cls, item: _AnyType) -> _AnyType:
        return Annotated[item, Depends(_DependsPlaceholder(item))]  # type: ignore


if TYPE_CHECKING:
    # The Injected type is used to mark types that must be overridden by the FastAPI app by way of
    # app.dependency_overrides[MyType] = wrap_dep_in_async_closure(...) in logfire_backend.api.create_app
    Injected = Annotated[
        _AnyType, ...
    ]  # Injected[T] will be recognized by type checkers as T
    """A dependency that is injected by FastAPI's dependency injection system.
    These are all bound in `main.create_app` so that they can be overridden in tests.
    """
else:
    Injected = InjectedTracker


def validate_injections(app: FastAPI) -> None:
    """Validate that all Injected types have been updated in app.dependency_overrides"""
    dependencies: list[Dependant] = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            dependencies.append(route.dependant)
            if route.dependency_overrides_provider is not app:
                raise RuntimeError(
                    "Route dependency overrides must be provided by the app itself"
                )
    # flatten
    stack = dependencies
    dependencies = []
    while stack:
        dep = stack.pop()
        for subdep in dep.dependencies:
            stack.append(subdep)
        dependencies.append(dep)

    calls = {
        dep.call.t for dep in dependencies if isinstance(dep.call, _DependsPlaceholder)
    }
    overrides = set(app.dependency_overrides.keys())

    missing_injections = list(calls - overrides)

    if missing_injections:
        raise RuntimeError(
            f"Missing dependency overrides for {missing_injections}."
            " Did you update `app.dependency_overrides` in `main.create_app`?"
        )


_T = TypeVar("_T")

def wrap_dep_in_async_closure(dep: Any) -> Any:
    """FastAPI runs sync deps in a thread so this creates an async lambda to wrap them."""

    async def wrapper() -> Any:
        return dep

    return wrapper


@overload
def bind(app: FastAPI, dep_type: Injected[_T], dep: _T) -> None:
    ...


@overload
def bind(app: FastAPI, dep_type: Any, dep: Any) -> None:
    ...


def bind(app: FastAPI, dep_type: type[_T], dep: _T) -> None:
    """Bind a dependency to the app for use in FastAPI's dependency injection system."""
    app.dependency_overrides[dep_type] = wrap_dep_in_async_closure(dep)
