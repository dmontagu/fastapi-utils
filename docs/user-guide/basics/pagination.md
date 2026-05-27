#### Source module: [`fastapi_utils.pagination`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/pagination.py){.internal-link target=_blank}

---

Many APIs expose list endpoints that need the same query parameters and response shape over and over.
The pagination utilities provide a reusable limit/offset dependency and a generic response model for those endpoints.

## Limit and offset pagination

Use `LimitOffsetParams` as a FastAPI dependency, then return a `Page` response with `paginate`:

```python hl_lines="4 21 22"
{!./src/pagination1.py!}
```

A request to `/users?limit=2&offset=1` returns:

```JSON
{
  "items": [
    {"id": 2, "name": "Grace"},
    {"id": 3, "name": "Linus"}
  ],
  "total": 4,
  "limit": 2,
  "offset": 1,
  "nextOffset": 3,
  "previousOffset": 0
}
```

The Python model fields use `snake_case`, while the generated OpenAPI schema and responses use `camelCase`,
matching the behavior of `APIModel`.
