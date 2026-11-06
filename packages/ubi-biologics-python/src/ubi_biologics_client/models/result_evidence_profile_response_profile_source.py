from enum import Enum


class ResultEvidenceProfileResponseProfileSource(str, Enum):
    CAPABILITY = "capability"
    TOOL = "tool"

    def __str__(self) -> str:
        return str(self.value)
