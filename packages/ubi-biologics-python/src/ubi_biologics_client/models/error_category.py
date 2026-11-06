from enum import Enum


class ErrorCategory(str, Enum):
    AUTHORIZATION = "authorization"
    CANCELLATION = "cancellation"
    CONFLICT = "conflict"
    INCOMPATIBILITY = "incompatibility"
    NOT_FOUND = "not_found"
    QUOTA = "quota"
    RETRYABLE_INFRASTRUCTURE = "retryable_infrastructure"
    TIMEOUT = "timeout"
    TOOL_FAILURE = "tool_failure"
    VALIDATION = "validation"

    def __str__(self) -> str:
        return str(self.value)
