from enum import Enum


class RunState(str, Enum):
    AWAITING_APPROVAL = "awaiting_approval"
    CANCELLED = "cancelled"
    CANCEL_REQUESTED = "cancel_requested"
    DRAFT = "draft"
    EXPIRED = "expired"
    FAILED = "failed"
    READY = "ready"
    REJECTED = "rejected"
    RUNNING = "running"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
