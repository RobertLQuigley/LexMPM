
from model.Base import Base
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy import Integer


class UserRoles(Base):
    __tablename__ = 'user_roles'
    __table_args__ = {"schema": "security"}
    user_id :Mapped[int] = mapped_column(Integer, foreign_key = "users.user_account.id", primary_key=True)
    role_id : Mapped[int] = mapped_column(Integer, foreign_key = "security.role.id", primary_key=True)

