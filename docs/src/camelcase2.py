from fastapi_restful.camelcase import camel2snake
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)


Base = declarative_base(cls=CustomBase)
