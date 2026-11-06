from enum import Enum


class ProjectListView(str, Enum):
    ALL = "all"
    FAVORITES = "favorites"
    RECENT = "recent"
    TRASH = "trash"

    def __str__(self) -> str:
        return str(self.value)
