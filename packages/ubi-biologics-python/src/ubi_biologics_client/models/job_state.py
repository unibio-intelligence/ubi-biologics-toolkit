from enum import Enum


class JobState(str, Enum):
    CANCELLED = "cancelled"
    CANCEL_REQUESTED = "cancel_requested"
    EXPIRED = "expired"
    FAILED = "failed"
    LEASED = "leased"
    QUEUED = "queued"
    RETRY_SCHEDULED = "retry_scheduled"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    TIMED_OUT = "timed_out"

    def __str__(self) -> str:
        return str(self.value)
