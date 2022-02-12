from typing import TYPE_CHECKING, Any, Callable, NoReturn, get_type_hints

from fastapi import APIRouter


class InferringRouter(APIRouter):
    """
    Overrides the route decorator logic to use the annotated return type as the `response_model` if unspecified.
    """

    if not TYPE_CHECKING:  # pragma: no branch

        def add_api_route(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
            if kwargs.get("response_model") is None:
                return_hint = get_type_hints(endpoint).get("return")
                if return_hint not in (NoReturn, type(None)):
                    kwargs["response_model"] = return_hint
            return super().add_api_route(path, endpoint, **kwargs)
