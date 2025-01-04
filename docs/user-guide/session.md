
#### Source module: [`fastapi_utils.sessions`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/session.py){.internal-link target=_blank}

!!! Note
    #### To use, please install with: `pip install fastapi-utils[session]` or `pip install fastapi-utils[all]`

One of the most commonly used ways to power database functionality with FastAPI is SQLAlchemy's ORM.

FastAPI has [great documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/) about how to integrate
ORM into your application.

However, the recommended approach for using SQLAlchemy's ORM with FastAPI has evolved over time to reflect both insights
from the community and the addition of new features to FastAPI.

The `fastapi_utils.session` module contains an implementation making use of the most up-to-date best practices for
managing SQLAlchemy sessions with FastAPI.

---

## `FastAPISessionMaker`

The `fastapi_utils.session.FastAPISessionMaker` class conveniently wraps session-making functionality for use with FastAPI. This section contains an example showing how to use this class.

### Step 1: Define the ORM Table  

First, ensure you have an ORM table to query:  

```
class User(Base):
    __tablename__ = "user"
    id = sa.Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = sa.Column(sa.String, nullable=False)

```

Here, the example sets up a basic table using SQLAlchemy. This table will act as the basis for database queries.

### Step 2: Configure the Database URI  

Next, set up infrastructure for loading the database URI from the environment:  

```
class DBSettings(BaseSettings):
    """Parses variables from environment on instantiation"""
    # This will automatically load the database URI from environment variables or a config file
    database_uri: str  # This should contain the URI of the database (e.g., 'postgresql://user:password@localhost/dbname')

    class Config:
        # Optional: this specifies the file that contains the environment variables (e.g., `.env` file)
        env_file = ".env"  # If you have an .env file, it will load from there automatically

```

We use the `pydantic.BaseSettings` to load variables from the environment. There is documentation for this class in the
<a href="https://pydantic-docs.helpmanual.io/usage/settings/" class="external-link" target="_blank">pydantic docs</a>,
but the basic idea is that if a model inherits from this class, any fields not specified during initialization
are read from the environment if possible.

!!! info
    Since `database_uri` is not an optional field, a `ValidationError` will be raised if the `DATABASE_URI` environment
    variable is not set.

!!! info
    For finer-grained control, you could remove the `database_uri` field, and replace it with
    separate fields for `scheme`, `username`, `password`, `host`, and `db`. You could then give the model a `@property`
    called `database_uri` that builds the URI from these components.

### Step 3: Create the `get_db` Dependency  

Now that we have a way to load the database URI, we can create the FastAPI dependency we'll use to obtain the SQLAlchemy session:

```
def get_db() -> Iterator[Session]:
    """FastAPI dependency that provides a SQLAlchemy session"""
    yield from _get_fastapi_sessionmaker().get_db()
```

This dependency provides an SQLAlchemy session for each request. It's designed to integrate seamlessly with FastAPI's dependency injection system.

!!! info
    The `get_db` dependency makes use of a context-manager dependency, rather than a middleware-based approach.  
    This means that any endpoints that don't make use of an SQLAlchemy session will not incur session-related overhead.  

    In contrast, middleware-based approaches create and close sessions for every request, even if the endpoint doesn't use them.

!!! warning
    The `get_db` dependency **will not finalize your ORM session until *after* a response is returned to the user.**  
    This has minor response-latency benefits, but also means that uncommitted database writes that cause errors may
    surface during request clean-up, after a success response (status code 200) is returned.

    To mitigate this, for any request where a database write might fail, **manually perform a commit in your endpoint logic and handle errors appropriately.**

    -----  

    Middleware-based approaches ensure database errors are visible to users but often result in generic 500 internal server errors. Strive to provide more informative error responses in production systems.  

    You can log database errors raised during cleanup by wrapping the `get_db` function in a `try-except` block.

### Step 4: Inject the Dependency  

The `get_db` function can be used as a FastAPI dependency, injecting an SQLAlchemy ORM session wherever required:  

The final Code example below:

```python hl_lines="45 46"
{!./src/session1.py!}
```

!!! info
    To optimize resource usage, the `_get_fastapi_sessionmaker` function is decorated with `@lru_cache`.  
    This ensures the same `FastAPISessionMaker` instance is reused across requests, reducing overhead.  

    The lazy initialization also ensures that modifications to environment variables (e.g., during testing) are reflected in new instances.

