from typing import Dict, Generic, List, TypeVar

from fastapi_utils.crud_base import CRUDBase, Base
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

ResponseModelType = TypeVar("ResponseModelType", bound=BaseModel)
ResponseModelManyType = TypeVar("ResponseModelManyType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
IDType = TypeVar("IDType")


def get_filter_fields(self) -> List[str]:
    """This would need to get overridden for each BaseRoute where the filter fields are defined.

    Returns:
        List[str] -- List of fields to filter by
    """
    return []


class BaseRoute(Generic[ResponseModelType, ResponseModelManyType, CreateSchemaType, UpdateSchemaType, IDType]):
    """A base route that has the basic CRUD endpoints.

    For read_many

    """

    filter_fields: List[str] = Depends(get_filter_fields)
    crud_base = CRUDBase(Base)  # type: ignore
    db: Session = Depends(None)
    object_name = "Base"

    def read_many(self, skip: int = 0, limit: int = 100, sort_by: str = None, **kwargs) -> ResponseModelManyType:
        """Reads many from the database with the provided filter and sort parameters.

        Filter parameters need to be specified by overriding this read_many method and calling it like:

            @router.get("/", response_model=List[Person])
            def read_persons(
                self, skip: int = 0, limit: int = 100, sort_by: str = None, name: str = None,
            ) -> List[Person]:
                return super().read_many(skip=skip, limit=limit, sort_by=sort_by, name=name)

        Where the filter fields are defined as parameters. In this case "name" is a filter field

        Keyword Arguments:
            skip {int} -- [description] (default: {0})
            limit {int} -- [description] (default: {100})
            sort_by {str} -- Expected in the form "model__field_name:asc,field_name:desc" (default: {None})

            **kwargs {str} -- Filter field names expected in the form field_name or model__field_name if filtering through
            a join. The filter is defined as op:value. For example ==:paul or eq:paul

            The filter op is specified in the crud_base FilterOpEnum.

        Returns:
            ResponseModelManyType -- [description]
        """
        filter_fields: Dict[str, str] = {}
        for field in self.filter_fields:
            filter_fields[field] = kwargs.pop(field, None)
        results = self.crud_base.get_multi(self.db, skip=skip, limit=limit, filter_by=filter_fields, sort_by=sort_by)
        return results

    def create(self, *, obj_in: CreateSchemaType,) -> ResponseModelType:
        """
        Create new object.
        """
        result = self.crud_base.create(db_session=self.db, obj_in=obj_in)
        return result

    def update(self, *, id: IDType, obj_in: UpdateSchemaType,) -> ResponseModelType:
        """
        Update an object.
        """
        result = self.crud_base.get(db_session=self.db, id=id)
        if not result:
            raise HTTPException(status_code=404, detail=f"{self.object_name} not found")
        # if not crud.user.is_superuser(current_user) and (object.owner_id != current_user.id):
        #     raise HTTPException(status_code=400, detail="Not enough permissions")
        result = self.crud_base.update(db_session=self.db, db_obj=result, obj_in=obj_in)
        return result

    def read(self, *, id: IDType,) -> ResponseModelType:
        """
        Get object by ID.
        """
        result = self.crud_base.get(db_session=self.db, id=id)
        if not result:
            raise HTTPException(status_code=404, detail=f"{self.object_name} not found")
        # if not crud.user.is_superuser(current_user) and (object.owner_id != current_user.id):
        #     raise HTTPException(status_code=400, detail="Not enough permissions")
        return result

    def delete(self, *, id: IDType,) -> ResponseModelType:
        """
        Delete an object.
        """
        result = self.crud_base.get(db_session=self.db, id=id)
        if not result:
            raise HTTPException(status_code=404, detail=f"{self.object_name} not found")
        # if not crud.user.is_superuser(current_user) and (object.owner_id != current_user.id):
        #     raise HTTPException(status_code=400, detail="Not enough permissions")
        result = self.crud_base.remove(db_session=self.db, id=id)
        return result
