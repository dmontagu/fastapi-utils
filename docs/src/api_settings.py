from fastapi import FastAPI

from fastapi_utils.api_settings import get_api_settings


def get_app() -> FastAPI:
    get_api_settings.cache_clear()
    settings = get_api_settings()
    app = FastAPI(**settings.fastapi_kwargs)
    # <Typically, you would include endpoint routers here>
    return app
