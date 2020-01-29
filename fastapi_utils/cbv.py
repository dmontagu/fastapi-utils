import functools
import inspect
from copy import deepcopy
from types import FunctionType
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, get_type_hints

from fastapi import APIRouter, Depends
from pydantic.typing import is_classvar
from starlette.routing import Route, WebSocketRoute

T = TypeVar("T")

CBV_CLASS_KEY = "__cbv_class__"
GENERIC_CBV_ROUTERS_KEY = "__generic_cbv_routers__"


def cbv(router: APIRouter) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        return _cbv(router, cls)

    return decorator


def generic_cbv(router: APIRouter) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        generic_routers = getattr(cls, GENERIC_CBV_ROUTERS_KEY, None)
        if generic_routers is None:
            generic_routers = []
            setattr(cls, GENERIC_CBV_ROUTERS_KEY, generic_routers)
        generic_routers.append(router)
        return cls

    return decorator


def _cbv(router: APIRouter, cls: Type[T]) -> Type[T]:
    _init_cbv(cls)
    cbv_router = APIRouter()
    functions = inspect.getmembers(cls, inspect.isfunction)
    routes_by_endpoint = _routes_by_endpoint(router)
    generic_routes_by_endpoint = {}
    for generic_router in getattr(cls, GENERIC_CBV_ROUTERS_KEY, []):
        generic_routes_by_endpoint.update(_routes_by_endpoint(generic_router))
    for _, func in functions:
        route = routes_by_endpoint.get(func)
        if route is None:
            route = generic_routes_by_endpoint.get(func)
            if route is None:
                continue
        else:
            router.routes.remove(route)
        route = deepcopy(route)
        route.endpoint = replace_method_with_copy(cls, func)
        _update_cbv_route_endpoint_signature(cls, route)
        cbv_router.routes.append(route)
    router.include_router(cbv_router)
    return cls


def _routes_by_endpoint(router: Optional[APIRouter]) -> Dict[Callable[..., Any], Union[Route, WebSocketRoute]]:
    return (
        {}
        if router is None
        else {route.endpoint: route for route in router.routes if isinstance(route, (Route, WebSocketRoute))}
    )


def _update_cbv_route_endpoint_signature(cls: Type[Any], route: Union[Route, WebSocketRoute]) -> None:
    old_endpoint = route.endpoint
    old_signature = inspect.signature(old_endpoint)
    old_parameters: List[inspect.Parameter] = list(old_signature.parameters.values())
    old_first_parameter = old_parameters[0]
    new_first_parameter = old_first_parameter.replace(default=Depends(cls))
    new_parameters = [new_first_parameter] + [
        parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY) for parameter in old_parameters[1:]
    ]
    new_signature = old_signature.replace(parameters=new_parameters)
    setattr(route.endpoint, "__signature__", new_signature)


def _init_cbv(cls: Type[Any]) -> None:
    if getattr(cls, CBV_CLASS_KEY, False):  # pragma: no cover
        return  # Already initialized
    old_init: Callable[..., Any] = cls.__init__
    old_signature = inspect.signature(old_init)
    old_parameters = list(old_signature.parameters.values())[1:]  # drop `self` parameter
    new_parameters = [
        x for x in old_parameters if x.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    dependency_names: List[str] = []
    for name, hint in get_type_hints(cls).items():
        if is_classvar(hint):
            continue
        parameter_kwargs = {}
        parameter_kwargs["default"] = getattr(cls, name, Ellipsis)
        dependency_names.append(name)
        new_parameters.append(
            inspect.Parameter(name=name, kind=inspect.Parameter.KEYWORD_ONLY, annotation=hint, **parameter_kwargs)
        )
    new_signature = old_signature.replace(parameters=new_parameters)

    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        for dep_name in dependency_names:
            dep_value = kwargs.pop(dep_name)
            setattr(self, dep_name, dep_value)
        old_init(self, *args, **kwargs)

    setattr(cls, "__signature__", new_signature)
    setattr(cls, "__init__", new_init)
    setattr(cls, CBV_CLASS_KEY, True)


def replace_method_with_copy(cls: Type[Any], function: FunctionType) -> FunctionType:
    copied = FunctionType(
        function.__code__,
        function.__globals__,
        name=function.__name__,
        argdefs=function.__defaults__,
        closure=function.__closure__,
    )
    functools.update_wrapper(copied, function)
    copied.__qualname__ = f"{cls.__name__}.{function.__name__}"
    copied.__kwdefaults__ = function.__kwdefaults__
    setattr(cls, function.__name__, copied)
    return copied
