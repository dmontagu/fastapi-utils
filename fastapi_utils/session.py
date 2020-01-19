from contextlib import contextmanager
from typing import Iterator, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session


class FastAPISessionMaker:
    def __init__(self, database_uri: str):
        self.database_uri = database_uri

        self._cached_engine: Optional[sa.engine.Engine] = None
        self._cached_sessionmaker: Optional[sa.orm.sessionmaker] = None

    @property
    def cached_engine(self) -> sa.engine.Engine:
        engine = self._cached_engine
        if engine is None:
            engine = self.get_new_engine()
            self._cached_engine = engine
        return engine

    @property
    def cached_sessionmaker(self) -> sa.orm.sessionmaker:
        sessionmaker = self._cached_sessionmaker
        if sessionmaker is None:
            sessionmaker = self.get_new_sessionmaker(self.cached_engine)
            self._cached_sessionmaker = sessionmaker
        return sessionmaker

    def get_new_engine(self,) -> sa.engine.Engine:
        return get_engine(self.database_uri)

    def get_new_sessionmaker(self, engine: Optional[sa.engine.Engine]) -> sa.orm.sessionmaker:
        engine = engine or self.cached_engine
        return get_sessionmaker_for_engine(engine)

    def get_db(self) -> Iterator[Session]:
        """
        Intended for use as a FastAPI dependency
        """
        yield from _get_db(self.cached_sessionmaker)

    @contextmanager
    def context_session(self) -> Iterator[Session]:
        yield from self.get_db()

    def reset_cache(self) -> None:
        self._cached_engine = None
        self._cached_sessionmaker = None


def get_engine(uri: str) -> sa.engine.Engine:
    return sa.create_engine(uri, pool_pre_ping=True)


def get_sessionmaker_for_engine(engine: sa.engine.Engine) -> sa.orm.sessionmaker:
    return sa.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def context_session(engine: sa.engine.Engine) -> Iterator[Session]:
    sessionmaker = get_sessionmaker_for_engine(engine)
    yield from _get_db(sessionmaker)


def _get_db(sessionmaker: sa.orm.sessionmaker) -> Iterator[Session]:
    session = sessionmaker()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()
