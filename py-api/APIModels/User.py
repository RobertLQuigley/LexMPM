from typing import Type

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from model.Users import UserAccount
import model.database as database

class UserIn(BaseModel):
    username: str
    password: str
    id: int
    fullname: str | None = None
    disabled: bool


class UserOut(BaseModel):
    username: str = ""
    id: int = 0
    disabled: bool | None = None
    full_name: str | None = None


def from_account_name( account_name: str) -> 'UserOut':
    session = Session(database.dbcontext.engine)
    user = session.query(UserAccount).filter(UserAccount.account_name == account_name).scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(
        username = user.account_name,
        id = user.id,
        disabled = user.disabled
    )


def from_db( ua: UserAccount | Type[UserAccount]) -> 'UserOut':
    if ua is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(
        username = ua.account_name,
        disabled = ua.disabled,
        id = ua.id
    )


def authenticate(session: Session, username: str, password: str) -> UserOut:
    user: Type[UserAccount] | None = session.query(UserAccount).filter_by(account_name=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.verify_password(password):
        raise HTTPException(status_code=404, detail="Incorrect password")
    return from_db(user)

