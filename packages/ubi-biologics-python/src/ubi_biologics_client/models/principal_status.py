from enum import Enum


class PrincipalStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    REVOKED = "revoked"

    def __str__(self) -> str:
        return str(self.value)
