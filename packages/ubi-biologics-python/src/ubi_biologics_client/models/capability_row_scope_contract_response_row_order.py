from enum import Enum


class CapabilityRowScopeContractResponseRowOrder(str, Enum):
    DATASET_VERSION_ORDER = "dataset_version_order"
    INLINE_ROW_ORDER = "inline_row_order"
    NOT_APPLICABLE = "not_applicable"
    SOURCE_SELECTION_ORDER = "source_selection_order"

    def __str__(self) -> str:
        return str(self.value)
