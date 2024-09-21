from enum import Enum, auto


class TasksGroup(Enum):
    feed = auto()

    def __str__(self):
        return self.name
