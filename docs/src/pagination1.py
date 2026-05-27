from fastapi import Depends, FastAPI
from pydantic import BaseModel

from fastapi_utils.pagination import LimitOffsetParams, Page, paginate

app = FastAPI()


class UserOut(BaseModel):
    id: int
    name: str


USERS = [
    UserOut(id=1, name="Ada"),
    UserOut(id=2, name="Grace"),
    UserOut(id=3, name="Linus"),
    UserOut(id=4, name="Margaret"),
]


@app.get("/users", response_model=Page[UserOut])
def list_users(params: LimitOffsetParams = Depends()) -> Page[UserOut]:
    return paginate(
        USERS[params.offset : params.offset + params.limit],
        total=len(USERS),
        params=params,
    )
