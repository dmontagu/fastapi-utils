from typing import TYPE_CHECKING, Any, Callable, get_type_hints

from fastapi import APIRouter


class InferringRouter(APIRouter):
    if not TYPE_CHECKING:

        def add_api_route(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
            if kwargs.get("response_model") is None:
                kwargs["response_model"] = get_type_hints(endpoint).get("return")
            return super().add_api_route(path, endpoint, **kwargs)

    else:  # pragma: no cover
        pass
