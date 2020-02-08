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
