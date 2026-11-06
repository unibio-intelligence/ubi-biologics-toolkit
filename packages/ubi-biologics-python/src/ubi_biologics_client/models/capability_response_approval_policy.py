from enum import Enum


class CapabilityResponseApprovalPolicy(str, Enum):
    ALWAYS = "always"
    NONE = "none"
    ORGANIZATION_POLICY = "organization_policy"

    def __str__(self) -> str:
        return str(self.value)
