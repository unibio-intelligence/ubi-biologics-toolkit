from enum import Enum


class FilterOperator(str, Enum):
    CONTAINS = "contains"
    ENDS_WITH = "ends_with"
    EQ = "eq"
    GT = "gt"
    GTE = "gte"
    IN = "in"
    IS_NOT_NULL = "is_not_null"
    IS_NULL = "is_null"
    LT = "lt"
    LTE = "lte"
    MATCHES_REGEX = "matches_regex"
    NE = "ne"
    SEQUENCE_AT = "sequence_at"
    STARTS_WITH = "starts_with"

    def __str__(self) -> str:
        return str(self.value)
