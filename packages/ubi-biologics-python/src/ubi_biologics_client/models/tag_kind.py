from enum import Enum


class TagKind(str, Enum):
    MANUAL = "manual"
    SMART = "smart"

    def __str__(self) -> str:
        return str(self.value)
