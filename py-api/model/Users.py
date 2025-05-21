from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  Integer, Unicode, ForeignKey, Boolean
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from model.Base import Base
from configuration.Security import pwd_context


class UserAccount(Base):
    __tablename__ = "user_account"
    __table_args__ = {"schema": "users"}
    id: Mapped[int] = mapped_column(Integer, primary_key=True,init=False)
    account_name: Mapped[str] = mapped_column(Unicode(100), nullable=False,init=True, unique=True)
    display_name: Mapped[str] = mapped_column(Unicode(100), nullable=False,init=True)
    password: Mapped[str] = mapped_column(Unicode(100), nullable=False, init=True)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    relationship("UserMetaData")

    def verify_password(self, password: str) -> bool:
        print(self.password)
        X = pwd_context.hash(self.password)
        pwd_context.verify_and_update(self.password, X)
        valid, new_hash =  pwd_context.verify_and_update(password,self.password)
        if valid:
            self.password = new_hash
            return True
        return False

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)


class UserMetaData(Base):
    __tablename__ = "user_metadata"
    __table_args__ = {"schema": "users"}
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(Unicode(100))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_account.id"))
    user: Mapped["UserAccount"] = relationship(default=None)
