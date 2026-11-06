from enum import Enum


class ResultEvidenceClass(str, Enum):
    COMPUTED_MEASUREMENT = "computed_measurement"
    EXPERIMENTAL = "experimental"
    HEURISTIC = "heuristic"
    PREDICTION = "prediction"

    def __str__(self) -> str:
        return str(self.value)
