import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from fastapi_utils.guid_type import GUID

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(GUID, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    related_id = sa.Column(GUID)  # a nullable, related field
