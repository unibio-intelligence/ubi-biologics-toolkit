from enum import Enum


class CapabilityRowScopeContractResponseEmptyScopePolicy(str, Enum):
    NOT_APPLICABLE = "not_applicable"
    REJECT = "reject"

    def __str__(self) -> str:
        return str(self.value)
