import sqlalchemy as sa
from fastapi_restful.guid_type import GUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(GUID, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    related_id = sa.Column(GUID)  # a nullable, related field
