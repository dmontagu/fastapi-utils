from typing import NewType, Optional
from uuid import UUID

import sqlalchemy as sa
from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.orm import Session, declarative_base
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from fastapi_utils.api_model import APIMessage, APIModel
from fastapi_utils.cbv import cbv
from fastapi_utils.guid_type import GUID
from fastapi_utils.inferring_router import InferringRouter

# Begin Setup
UserID = NewType("UserID", UUID)
ItemID = NewType("ItemID", UUID)

Base = declarative_base()


class ItemORM(Base):
    __tablename__ = "item"

    item_id = sa.Column(GUID, primary_key=True)
    owner = sa.Column(GUID, nullable=False)
    name = sa.Column(sa.String, nullable=False)


class ItemCreate(APIModel):
    name: str
    owner: UserID


class ItemInDB(ItemCreate):
    item_id: ItemID


def get_jwt_user(authorization: str = Header(...)) -> UserID:
    """Pretend this function gets a UserID from a JWT in the auth header"""


def get_db() -> Session:
    """Pretend this function returns a SQLAlchemy ORM session"""


def get_owned_item(session: Session, owner: UserID, item_id: ItemID) -> ItemORM:
    item: Optional[ItemORM] = session.get(ItemORM, item_id)
    if item is not None and item.owner != owner:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)
    if item is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return item


# End Setup
app = FastAPI()
router = InferringRouter()  # Step 1: Create a router


@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class ItemCBV:
    # Step 3: Add dependencies as class attributes
    session: Session = Depends(get_db)
    user_id: UserID = Depends(get_jwt_user)

    @router.post("/item")
    def create_item(self, item: ItemCreate) -> ItemInDB:
        # Step 4: Use `self.<dependency_name>` to access shared dependencies
        item_orm = ItemORM(name=item.name, owner=self.user_id)
        self.session.add(item_orm)
        self.session.commit()
        return ItemInDB.from_orm(item_orm)

    @router.get("/item/{item_id}")
    def read_item(self, item_id: ItemID) -> ItemInDB:
        item_orm = get_owned_item(self.session, self.user_id, item_id)
        return ItemInDB.from_orm(item_orm)

    @router.put("/item/{item_id}")
    def update_item(self, item_id: ItemID, item: ItemCreate) -> ItemInDB:
        item_orm = get_owned_item(self.session, self.user_id, item_id)
        item_orm.name = item.name
        self.session.add(item_orm)
        self.session.commit()
        return ItemInDB.from_orm(item_orm)

    @router.delete("/item/{item_id}")
    def delete_item(self, item_id: ItemID) -> APIMessage:
        item = get_owned_item(self.session, self.user_id, item_id)
        self.session.delete(item)
        self.session.commit()
        return APIMessage(detail=f"Deleted item {item_id}")


app.include_router(router)
