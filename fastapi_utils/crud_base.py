from decimal import Decimal
from enum import Enum
from typing import Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi_utils.camelcase import snake2camel
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_filters import apply_filters, apply_sort

Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
MultiSchemaType = TypeVar("MultiSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
IDType = TypeVar("IDType")


class SortDirectionEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"


class FilterOpEnum(str, Enum):
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    EQ_SYM = "=="
    EQ = "eq"
    NE_SYM = "!="
    NE = "ne"
    GT_SYM = ">"
    GT = "gt"
    LT_SYM = "<"
    LT = "lt"
    GE_SYM = ">="
    GE = "ge"
    LE_SYM = "<="
    LE = "le"
    LIKE = "like"
    ILIKE = "ilike"
    IN = "in"
    NOT_IN = "not_in"


class SortField(BaseModel):
    field: str
    model: Optional[str] = None
    direction: SortDirectionEnum = SortDirectionEnum.DESC


class FilterField(BaseModel):
    field: str
    model: Optional[str] = None
    op: FilterOpEnum
    value: Union[str, int, Decimal]


def get_filter_field(field: str, field_name: str, split_character: str = ":") -> FilterField:
    model = None
    op, value = field.split(":")
    if "__" in field_name:
        model, field_name = field_name.split("__")
        model = snake2camel(model, start_lower=False)
    filter_field = FilterField(field=field_name, model=model, op=op, value=value)
    return filter_field


def get_filter_fields(fields: Optional[Dict[str, str]], split_character: str = ":") -> List[FilterField]:
    filter_fields = []
    if fields:
        for field_name in fields:
            if fields[field_name]:
                filter_fields.append(get_filter_field(field=fields[field_name], field_name=field_name))
    return filter_fields


def get_sort_field(field: str) -> SortField:
    model = None
    field_name, direction = field.split(":")
    if "__" in field_name:
        model, field_name = field_name.split("__")
    sort_field = SortField(model=model, field=field_name, direction=direction)
    return sort_field


def get_sort_fields(sort_string: str, split_character: str = ",") -> List[SortField]:
    sort_fields = []
    # There could be many sort fields
    if sort_string:
        sort_by_fields = sort_string.split(",")
        for _to_sort in sort_by_fields:
            sort_fields.append(get_sort_field(_to_sort))
    return sort_fields


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db_session: Session, id: IDType) -> Optional[ModelType]:
        return db_session.query(self.model).filter(self.model.id == id).first()  # type: ignore

    def get_multi(
        self,
        db_session: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None,
        filter_by: Optional[Dict[str, str]] = None,
    ) -> List[ModelType]:

        sort_spec_pydantic = get_sort_fields(sort_by)
        filter_spec_pydantic = get_filter_fields(filter_by)

        sort_spec = [x.dict(exclude_none=True) for x in sort_spec_pydantic]
        filter_spec = [x.dict(exclude_none=True) for x in filter_spec_pydantic]

        query = db_session.query(self.model)
        query = apply_filters(query, filter_spec)
        query = apply_sort(query, sort_spec)

        count = query.count()
        query = query.offset(skip).limit(limit)

        return query.all()

    def create(self, db_session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(self, db_session: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(skip_defaults=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def remove(self, db_session: Session, *, id: IDType) -> ModelType:
        obj = db_session.query(self.model).get(id)
        db_session.delete(obj)
        db_session.commit()
        return obj
