from typing import Any, Callable, get_type_hints

import fastapi.exceptions
import fastapi.utils
from fastapi import APIRouter


class InferringRouter(APIRouter):
    """
    Overrides the route decorator logic to use the annotated return type as the `response_model` if unspecified.
    """

    def add_api_route(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
        if kwargs.get("response_model") is None:
            return_annotation = get_type_hints(endpoint).get("return")
            if return_annotation is not None:
                try:
                    fastapi.utils.create_response_field("", return_annotation)
                except fastapi.exceptions.FastAPIError:
                    # The return type is not a valid `response_model`
                    pass
                else:
                    kwargs["response_model"] = return_annotation
        return super().add_api_route(path, endpoint, **kwargs)
