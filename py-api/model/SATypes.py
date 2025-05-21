from enum import Enum as PyEnum

class ProjectStatus(PyEnum):
    new = 1
    analysis = 2
    in_progress = 3
    complete = 4
    canceled = 5
    postponed = 6

class TaskStatus(PyEnum):
    new = 1
    assigned = 2
    in_progress = 3
    complete = 4
    cancelled = 5
    postponed = 6
