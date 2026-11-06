from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.sort_direction import SortDirection
from ..types import UNSET, Unset

T = TypeVar("T", bound="SortExpression")


@_attrs_define
class SortExpression:
    """
    Attributes:
        field (str):
        direction (SortDirection | Unset):
    """

    field: str
    direction: SortDirection | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        direction: str | Unset = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "field": field,
            }
        )
        if direction is not UNSET:
            field_dict["direction"] = direction

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field")

        _direction = d.pop("direction", UNSET)
        direction: SortDirection | Unset
        if isinstance(_direction, Unset):
            direction = UNSET
        else:
            direction = SortDirection(_direction)

        sort_expression = cls(
            field=field,
            direction=direction,
        )

        return sort_expression
