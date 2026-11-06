from enum import Enum


class CapabilityRowScopeContractResponseScopeBinding(str, Enum):
    DATASET_VERSION = "dataset_version"
    INLINE_ROWS = "inline_rows"
    NOT_APPLICABLE = "not_applicable"
    RESOURCE_BINDING = "resource_binding"
    ROW_PARAMETERS = "row_parameters"
    SELECTION_OR_DATASET_VERSION = "selection_or_dataset_version"

    def __str__(self) -> str:
        return str(self.value)
