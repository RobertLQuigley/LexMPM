from typing import List

from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy import Integer, Unicode, Boolean, ForeignKey
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from model.Base import Base



class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"schema": "security"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(Unicode(100), nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)