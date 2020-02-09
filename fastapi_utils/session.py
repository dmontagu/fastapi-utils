from contextlib import contextmanager
from typing import Iterator, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session


class FastAPISessionMaker:
    """
    This class provides a convenient cached interface for accessing sqlalchemy ORM sessions using just a database URI.

    The expected format of database_uri is `"<scheme>://<user>:<password>@<host>:<port>/<database>`, exactly as you'd
    use with `sqlalchemy.create_engine`.

    For example, if a postgres database named `app` is accessible on a container named `db`,
    the `database_uri` might look like: "postgresql://db_user:password@db:5432/app"
    """

    def __init__(self, database_uri: str):
        self.database_uri = database_uri

        self._cached_engine: Optional[sa.engine.Engine] = None
        self._cached_sessionmaker: Optional[sa.orm.sessionmaker] = None

    @property
    def cached_engine(self) -> sa.engine.Engine:
        """
        Returns the cached engine if present, or a new (cached) engine using the database_uri if not
        """
        engine = self._cached_engine
        if engine is None:
            engine = self.get_new_engine()
            self._cached_engine = engine
        return engine

    @property
    def cached_sessionmaker(self) -> sa.orm.sessionmaker:
        """
        Returns the cached sessionmaker if present, or a new (cached) sessionmaker using the cached_engine if not
        """
        sessionmaker = self._cached_sessionmaker
        if sessionmaker is None:
            sessionmaker = self.get_new_sessionmaker(self.cached_engine)
            self._cached_sessionmaker = sessionmaker
        return sessionmaker

    def get_new_engine(self) -> sa.engine.Engine:
        """
        Returns a new sqlalchemy engine for the database_uri.
        """
        return get_engine(self.database_uri)

    def get_new_sessionmaker(self, engine: Optional[sa.engine.Engine]) -> sa.orm.sessionmaker:
        """
        Returns a new sessionmaker for the (optional) provided engine.

        If `None` is provided, the cached engine is used. (A new engine is created and cached if necessary.)
        """
        engine = engine or self.cached_engine
        return get_sessionmaker_for_engine(engine)

    def get_db(self) -> Iterator[Session]:
        """
        A FastAPI dependency that yields a sqlalchemy session.

        The session is created by the cached sessionmaker, and closed via contextmanager after the response is returned.

        Note that if you perform any database writes and want to handle errors *prior* to returning a response (and you
        should!), you'll need to put `session.commit()` or `session.rollback()` as appropriate in your endpoint code.
        This is generally a best practice for expected errors anyway since otherwise you would generate a 500 response.
        """
        yield from _get_db(self.cached_sessionmaker)

    @contextmanager
    def context_session(self) -> Iterator[Session]:
        """
        This method directly produces a context-managed session without relying on FastAPI's dependency injection.

        Usage would look like:
        ```python
        session_maker = FastAPISessionMaker(db_uri)
        with session_maker.context_session() as session:
            instance = session.query(OrmModel).get(instance_id)
        ```
        """
        yield from self.get_db()

    def reset_cache(self) -> None:
        """
        Resets the engine and sessionmaker caches.

        After calling this method, the next time you try to use the cached engine or sessionmaker,
        new ones will be created.
        """
        self._cached_engine = None
        self._cached_sessionmaker = None


def get_engine(uri: str) -> sa.engine.Engine:
    """
    Returns a new sqlalchemy engine that "tests connections for liveness upon each checkout".
    """
    return sa.create_engine(uri, pool_pre_ping=True)


def get_sessionmaker_for_engine(engine: sa.engine.Engine) -> sa.orm.sessionmaker:
    """
    Returns a sqlalchemy sessionmaker for the provided engine, using recommended settings for use with FastAPI.
    """
    return sa.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def context_session(engine: sa.engine.Engine) -> Iterator[Session]:
    """
    This method produces a context-managed session for use with a specified engine.

    Behaves similarly to FastAPISessionMaker.context_session.
    """
    sessionmaker = get_sessionmaker_for_engine(engine)
    yield from _get_db(sessionmaker)


def _get_db(sessionmaker: sa.orm.sessionmaker) -> Iterator[Session]:
    """
    The underlying generator function used to create context-managed sqlalchemy sessions for:
    * context_session
    * FastAPISessionMaker.context_session
    * FastAPISessionMaker.get_db
    """
    session = sessionmaker()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()
