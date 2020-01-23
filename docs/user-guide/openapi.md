#### Source module: [`fastapi_utils.openapi`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/openapi.py){.internal-link target=_blank}

---

One of the biggest benefits of working with FastAPI is the auto-generated OpenAPI spec, which enables
integration with a variety of API development and documentation tooling, like Swagger UI and Redoc.

A particularly powerful application of the OpenAPI spec is using it to generate an API client.

The `openapi-generator` project makes it easy to generate API clients for a variety of languages based
entirely on your OpenAPI spec. This is especially useful in situations where your server and client are
implemented in different languages, or you have multiple clients to maintain (e.g., for native mobile apps).
Using a generated client makes it easy to keep your client in sync with your server as you add or refactor endpoints.

Typically, `openapi-generator` will use an endpoint's `operationId` to generate the name for the client function
that hits the associated endpoint.

When generating the OpenAPI spec, by default FastAPI includes the function name, endpoint path, and request method,
in the generated `operationId`:

```python hl_lines="13"
{!./src/openapi1.py!}
```

This is a good default behavior because it ensures that distinct endpoints on your server
will have distinct `operationId`s. However, it also means that an auto-generated client will have
extremely verbose function names like `getResourceApiV1ResourceResourceIdGet`.

To simplify your operation IDs, you can use `fastapi_utils.openapi.simplify_operation_ids` to replace
the generated operation IDs with ones generated using *only* the function name:

```python hl_lines="3 13 17"
{!./src/openapi2.py!}
```

Note that this requires you to use different function names for each endpoint/method combination, or you
will end up with conflicting `operationId`s. But this is usually pretty easy to ensure, and can 
significantly improve the naming used by your auto-generated API client(s).
