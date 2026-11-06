from enum import Enum


class ProjectRole(str, Enum):
    EDITOR = "editor"
    MANAGER = "manager"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)
