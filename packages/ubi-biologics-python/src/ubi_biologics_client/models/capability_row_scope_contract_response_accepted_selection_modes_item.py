from enum import Enum


class CapabilityRowScopeContractResponseAcceptedSelectionModesItem(str, Enum):
    ALL_ROWS = "all_rows"
    EXPLICIT_ROWS = "explicit_rows"
    FILTERED_ROWS = "filtered_rows"
    RANGE_ROWS = "range_rows"
    SINGLE_ROW = "single_row"
    VISIBLE_ROWS = "visible_rows"

    def __str__(self) -> str:
        return str(self.value)
