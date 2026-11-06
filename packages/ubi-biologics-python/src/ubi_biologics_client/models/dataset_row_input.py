from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_row_input_values import DatasetRowInputValues


T = TypeVar("T", bound="DatasetRowInput")


@_attrs_define
class DatasetRowInput:
    """
    Attributes:
        values (DatasetRowInputValues):
        logical_row_id (None | str | Unset):
    """

    values: DatasetRowInputValues
    logical_row_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        values = self.values.to_dict()

        logical_row_id: None | str | Unset
        if isinstance(self.logical_row_id, Unset):
            logical_row_id = UNSET
        else:
            logical_row_id = self.logical_row_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "values": values,
            }
        )
        if logical_row_id is not UNSET:
            field_dict["logical_row_id"] = logical_row_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_row_input_values import DatasetRowInputValues

        d = dict(src_dict)
        values = DatasetRowInputValues.from_dict(d.pop("values"))

        def _parse_logical_row_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logical_row_id = _parse_logical_row_id(d.pop("logical_row_id", UNSET))

        dataset_row_input = cls(
            values=values,
            logical_row_id=logical_row_id,
        )

        return dataset_row_input
