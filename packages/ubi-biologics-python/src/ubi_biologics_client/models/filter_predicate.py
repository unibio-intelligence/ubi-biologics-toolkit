from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.filter_operator import FilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterPredicate")


@_attrs_define
class FilterPredicate:
    """
    Attributes:
        field (str):
        operator (FilterOperator):
        value (Any | Unset):
    """

    field: str
    operator: FilterOperator
    value: Any | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        operator = self.operator.value

        value = self.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "field": field,
                "operator": operator,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field")

        operator = FilterOperator(d.pop("operator"))

        value = d.pop("value", UNSET)

        filter_predicate = cls(
            field=field,
            operator=operator,
            value=value,
        )

        return filter_predicate
