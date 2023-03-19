from sqlalchemy.orm import declarative_base, declared_attr

from fastapi_utils.camelcase import camel2snake


class CustomBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)


Base = declarative_base(cls=CustomBase)
