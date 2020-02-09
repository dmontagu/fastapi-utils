#### Source module: [`fastapi_utils.sessions`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/session.py){.internal-link target=_blank}

---

One of the most commonly used ways to power database functionality with FastAPI is SQLAlchemy's ORM.

FastAPI has [great documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/) about how to integrate
ORM into your application.

However, the recommended approach for using SQLAlchemy's ORM with FastAPI has evolved over time to reflect both insights
from the community and the addition of new features to FastAPI.

The `fastapi_utils.session` module contains an implementation making use of the most up-to-date best practices for
managing SQLAlchemy sessions with FastAPI.

---

## `FastAPISessionMaker`
The `fastapi_utils.session.FastAPISessionMaker` class conveniently wraps session-making functionality for use with
FastAPI. This section contains an example showing how to use this class. 

Let's begin with some infrastructure. The first thing we'll do is make sure we have an ORM
table to query:  

```python hl_lines="8 9 11 14 17 18 19 20"
{!./src/session1.py!}
```

Next, we set up infrastructure for loading the database uri from the environment:

```python hl_lines="23 24 25 26"
{!./src/session1.py!}
```

We use the `pydantic.BaseSettings` to load variables from the environment. There is documentation for this class in the
<a href="https://pydantic-docs.helpmanual.io/usage/settings/" class="external-link" target="_blank">pydantic docs</a>,
but the basic idea is that if a model inherits from this class, any fields not specified during initialization
are read from the environment if possible.

!!! info
    Since `database_uri` is not an optional field, a `ValidationError` will be raised if the `DATABASE_URI` environment
    variable is not set.

!!! info
    For finer grained control, you could remove the `database_uri` field, and replace it with
    separate fields for `scheme`, `username`, `password`, `host`, and `db`. You could then give the model a `@property`
    called `database_uri` that builds the uri from these components.

Now that we have a way to load the database uri, we can create the FastAPI dependency we'll use
to obtain the sqlalchemy session:

```python hl_lines="29 30 31 34 35 36 37 38"
{!./src/session1.py!}
```

!!! info
    The `get_db` dependency makes use of a context-manager dependency, rather than a middleware-based approach.
    This means that any endpoints that don't make use of a sqlalchemy session will not be exposed to any
    session-related overhead.
    
    This is in contrast with middleware-based approaches, where the handling of every request would result in
    a session being created and closed, even if the endpoint would not make use of it. 

!!! warning
    The `get_db` dependency **will not finalize your ORM session until *after* a response is returned to the user**.
    
    This has minor response-latency benefits, but also means that if you have any uncommitted
    database writes that will raise errors, you may return a success response to the user (status code 200),
    but still raise an error afterward during request clean-up.

    To deal with this, for any request where you expect a database write to potentially fail, you should **manually
    perform a commit inside your endpoint logic and appropriately handle any resulting errors.**

    -----
    
    Note that while middleware-based approaches can automatically ensure database errors are visible to users, the
    result would be a generic 500 internal server error, which you should strive to avoid sending to clients under
    normal circumstances.

    You can still log any database errors raised during cleanup by appropriately modifying the `get_db` function
    with a `try: except:` block.

The `get_db` function can be used as a FastAPI dependency that will inject a sqlalchemy ORM session where used:

```python hl_lines="45 46"
{!./src/session1.py!}
```

!!! info
    We make use of `@lru_cache` on `_get_fastapi_sessionmaker` to ensure the same `FastAPISessionMaker` instance is
    reused across requests. This reduces the per-request overhead while still ensuring the instance is created
    lazily, making it possible to have the `database_uri` reflect modifications to the environment performed *after*
    importing the relevant source file.
    
    This can be especially useful during testing if you want to override environment variables programmatically using
    your testing framework.
