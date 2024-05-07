from typing import NewType, Optional
from uuid import UUID

import sqlalchemy as sa
from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from fastapi_utils.api_model import APIMessage, APIModel
from fastapi_utils.guid_type import GUID

# Begin setup
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


class ItemInDB(ItemCreate):
    item_id: ItemID
    owner: UserID


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


# End setup
app = FastAPI()


@app.post("/item", response_model=ItemInDB)
def create_item(
    *,
    session: Session = Depends(get_db),
    user_id: UserID = Depends(get_jwt_user),
    item: ItemCreate,
) -> ItemInDB:
    item_orm = ItemORM(name=item.name, owner=user_id)
    session.add(item_orm)
    session.commit()
    return ItemInDB.from_orm(item_orm)


@app.get("/item/{item_id}", response_model=ItemInDB)
def read_item(
    *,
    session: Session = Depends(get_db),
    user_id: UserID = Depends(get_jwt_user),
    item_id: ItemID,
) -> ItemInDB:
    item_orm = get_owned_item(session, user_id, item_id)
    return ItemInDB.from_orm(item_orm)


@app.put("/item/{item_id}", response_model=ItemInDB)
def update_item(
    *,
    session: Session = Depends(get_db),
    user_id: UserID = Depends(get_jwt_user),
    item_id: ItemID,
    item: ItemCreate,
) -> ItemInDB:
    item_orm = get_owned_item(session, user_id, item_id)
    item_orm.name = item.name
    session.add(item_orm)
    session.commit()
    return ItemInDB.from_orm(item_orm)


@app.delete("/item/{item_id}", response_model=APIMessage)
def delete_item(
    *,
    session: Session = Depends(get_db),
    user_id: UserID = Depends(get_jwt_user),
    item_id: ItemID,
) -> APIMessage:
    item = get_owned_item(session, user_id, item_id)
    session.delete(item)
    session.commit()
    return APIMessage(detail=f"Deleted item {item_id}")
