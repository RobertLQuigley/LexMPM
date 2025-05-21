from model.Base import Base
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy import  Integer


class ProjectTasks(Base):
    __tablename__ = 'project_tasks'
    __table_args__ = {"schema": "pm"}
    project_id :Mapped[int] = mapped_column(Integer, foreign_key = "pm.project.id", primary_key=True)
    task_id : Mapped[int] = mapped_column(Integer, foreign_key = "pm.task.id", primary_key=True)

