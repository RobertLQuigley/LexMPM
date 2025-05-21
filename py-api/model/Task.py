from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from model.Base import Base
from model.SATypes import TaskStatus

class Task(Base):
    __tablename__ = 'project'
    __table_args__ = {'schema', 'pm' }

    id: Mapped[int] = mapped_column(Integer, primary_key=True,init=False)
    name: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.new)