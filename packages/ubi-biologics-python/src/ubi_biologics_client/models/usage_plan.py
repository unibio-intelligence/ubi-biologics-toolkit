from enum import Enum


class UsagePlan(str, Enum):
    ENTERPRISE = "enterprise"
    FREE = "free"
    PRO = "pro"

    def __str__(self) -> str:
        return str(self.value)
