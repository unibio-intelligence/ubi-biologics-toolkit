from enum import Enum


class CapabilityRowScopeContractResponseOperationLevel(str, Enum):
    PARAMETER_ONLY = "parameter_only"
    RESOURCE = "resource"
    ROW = "row"

    def __str__(self) -> str:
        return str(self.value)
