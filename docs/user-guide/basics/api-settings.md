#### Source module: [`fastapi_utils.api_settings`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/api_settings.py){.internal-link target=_blank}

---

The `BaseSettings` class provided as part of pydantic makes it very easy to load variables
from the environment for use as part of application configuration.

This package provides a class called `APISettings` which makes it easy to set the most
common configuration settings used with FastAPI through environment variables.

It also provides an `lru_cache`-decorated function for accessing a cached settings
instance to ensure maximum performance if you want to access the settings in endpoint
functions.

Even if you care about different settings in your own application, you can follow
the patterns in `fastapi_utils.api_settings` to efficiently access environment-determined
application configuration settings.

### Settings provided by `APISettings`:

When initialized, `APISettings` reads the following environment variables into the specified attributes:

Environment Variable | Attribute Name   | Type   | Default Value
-------------------- | ---------------- | ------ | -------------
`API_DEBUG`          | `debug`          | `bool` | `False`
`API_DOCS_URL`       | `docs_url`       | `str`  | `"/docs`
`API_OPENAPI_PREFIX` | `openapi_prefix` | `str`  | `""`
`API_OPENAPI_URL`    | `openapi_url`    | `str`  | `"/openapi.json"`
`API_REDOC_URL`      | `redoc_url`      | `str`  | `"/redoc"`
`API_TITLE`          | `title`          | `str`  | `"FastAPI"`
`API_VERSION`        | `version`        | `str`  | `"0.1.0"`
`API_DISABLE_DOCS`   | `disable_docs`   | `bool` | `False`

`APISettings` also has a derived property `fastapi_kwargs` consisting of a dict with all of the attributes above except
`disable_docs`.

(Note that each of the keys of `fastapi_kwargs` are keyword arguments for `fastapi.FastAPI.__init__`.)

If `disable_docs` is `True`, the values of `docs_url`, `redoc_url`, and `openapi_url` are all set to `None`
in the `fastapi_kwargs` property value.


### Using `APISettings` to configure a `FastAPI` instance

It is generally a good idea to initialize your `FastAPI` instance inside a function.
This ensures that you never have access to a partially-configured instance of your app,
and you can easily change settings and generate a new instance (for example during tests).

Here's a simple example of what this might look like:

```python hl_lines="3"
{!./src/api_settings.py!}
```

The `get_api_settings` just returns an instance of `APISettings`, but it is decorated with `lru_cache`
to ensure that the expensive operation of reading and parsing environment variables is only
done once, even if you were to frequently access the settings in endpoint code.

However, we can make sure that settings are reloaded whenever the app is created by adding
`get_api_settings.cache_clear()` to the app creation function, which resets the `lru_cache`:

```python hl_lines="7"
{!./src/api_settings.py!}
```

You can then reload (and cache) the environment settings by calling `get_api_settings()`,
and can get environment-determined keyword arguments for `FastAPI` from `api_settings.fastapi_kwargs`:

```python hl_lines="8 9"
{!./src/api_settings.py!}
```

If none of the relevant environment variables are set, the resulting instance would have
been initialized with the default keyword arguments of `FastAPI`.

But, for example, if the `API_DISABLE_DOCS` environment variable had the value `"true"`,
then the result of `get_app()` would be a `FastAPI` instance where `docs_url`, `redoc_url`,
and `openapi_url` are all `None` (and the API docs are secure).

This might be useful if you want to enable docs during development, but hide your OpenAPI schema
and disable the docs endpoints in production.
