from enum import Enum


class RunMode(str, Enum):
    EXECUTE = "execute"
    PREVIEW = "preview"

    def __str__(self) -> str:
        return str(self.value)
