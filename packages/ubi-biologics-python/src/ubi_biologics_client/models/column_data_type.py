from enum import Enum


class ColumnDataType(str, Enum):
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    INTEGER = "integer"
    JSON = "json"
    NUMBER = "number"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
