from enum import Enum


class SideEffectClass(str, Enum):
    DESTRUCTIVE = "destructive"
    EXPENSIVE_COMPUTE = "expensive_compute"
    EXTERNAL_WRITE = "external_write"
    READ_ONLY = "read_only"
    REVERSIBLE_WRITE = "reversible_write"

    def __str__(self) -> str:
        return str(self.value)
