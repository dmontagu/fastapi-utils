from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from fastapi import FastAPI

from fastapi_utils.api_model import APIModel

UserID = NewType("UserID", UUID)


class User(APIModel):
    user_id: UserID
    email_address: str


@dataclass
class UserORM:
    """
    You can pretend this class is a SQLAlchemy model
    """

    user_id: UserID
    email_address: str


app = FastAPI()


@app.post("/users", response_model=User)
async def create_user(user: User) -> UserORM:
    return UserORM(user.user_id, user.email_address)
