from enum import Enum


class JobAttemptState(str, Enum):
    CANCELLED = "cancelled"
    FAILED = "failed"
    LEASED = "leased"
    LEASE_EXPIRED = "lease_expired"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    TIMED_OUT = "timed_out"

    def __str__(self) -> str:
        return str(self.value)
