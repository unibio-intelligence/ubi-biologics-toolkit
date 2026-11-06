from enum import Enum


class ResourceKind(str, Enum):
    ARTIFACT = "artifact"
    ASSET = "asset"
    DATASET = "dataset"
    DATASET_VERSION = "dataset_version"
    INLINE = "inline"
    PICK_LIST = "pick_list"
    REFERENCE = "reference"
    SELECTION = "selection"

    def __str__(self) -> str:
        return str(self.value)
