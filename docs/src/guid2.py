import sqlalchemy as sa

from fastapi_utils.guid_type import setup_guids_postgresql

database_uri = "postgresql://user:password@db:5432/app"
engine = sa.create_engine(database_uri)
setup_guids_postgresql(engine)
