#### Source module: [`fastapi_utils.camelcase`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/camelcase.py){.internal-link target=_blank}

---

The `fastapi_utils.camelcase` module contains functions for converting `camelCase` or `CamelCase`
strings to `snake_case`, and vice versa:

```python hl_lines=""
{!./src/camelcase1.py!}
``` 

These functions are used by [APIModel](api-model.md) to ensure `snake_case` can be used in your python code,
and `camelCase` attributes in external `JSON`.

But they can also come in handy in other places -- for example, you could use them to ensure tables
declared using SQLAlchemy's declarative API are named using `snake_case`:

```python hl_lines=""
{!./src/camelcase2.py!}
``` 

If you were to create a `class MyUser(Base):` using `Base` defined above,
the resulting database table would be named `my_user`.
