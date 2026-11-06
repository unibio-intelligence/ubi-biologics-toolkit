from enum import Enum


class RowTagResponseAssignmentSource(str, Enum):
    MANUAL = "manual"
    MANUAL_AND_SMART = "manual_and_smart"
    SMART = "smart"

    def __str__(self) -> str:
        return str(self.value)
