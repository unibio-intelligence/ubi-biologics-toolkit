from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.column_data_type import ColumnDataType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_column_definition_display import (
        DatasetColumnDefinitionDisplay,
    )
    from ..models.dataset_column_definition_provenance import (
        DatasetColumnDefinitionProvenance,
    )


T = TypeVar("T", bound="DatasetColumnDefinition")


@_attrs_define
class DatasetColumnDefinition:
    """
    Attributes:
        data_type (ColumnDataType):
        key (str):
        label (str):
        semantic_type (str):
        display (DatasetColumnDefinitionDisplay | Unset):
        is_system (bool | Unset):  Default: False.
        nullable (bool | Unset):  Default: True.
        provenance (DatasetColumnDefinitionProvenance | Unset):
        unit (None | str | Unset):
    """

    data_type: ColumnDataType
    key: str
    label: str
    semantic_type: str
    display: DatasetColumnDefinitionDisplay | Unset = UNSET
    is_system: bool | Unset = False
    nullable: bool | Unset = True
    provenance: DatasetColumnDefinitionProvenance | Unset = UNSET
    unit: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        data_type = self.data_type.value

        key = self.key

        label = self.label

        semantic_type = self.semantic_type

        display: dict[str, Any] | Unset = UNSET
        if not isinstance(self.display, Unset):
            display = self.display.to_dict()

        is_system = self.is_system

        nullable = self.nullable

        provenance: dict[str, Any] | Unset = UNSET
        if not isinstance(self.provenance, Unset):
            provenance = self.provenance.to_dict()

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data_type": data_type,
                "key": key,
                "label": label,
                "semantic_type": semantic_type,
            }
        )
        if display is not UNSET:
            field_dict["display"] = display
        if is_system is not UNSET:
            field_dict["is_system"] = is_system
        if nullable is not UNSET:
            field_dict["nullable"] = nullable
        if provenance is not UNSET:
            field_dict["provenance"] = provenance
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_column_definition_display import (
            DatasetColumnDefinitionDisplay,
        )
        from ..models.dataset_column_definition_provenance import (
            DatasetColumnDefinitionProvenance,
        )

        d = dict(src_dict)
        data_type = ColumnDataType(d.pop("data_type"))

        key = d.pop("key")

        label = d.pop("label")

        semantic_type = d.pop("semantic_type")

        _display = d.pop("display", UNSET)
        display: DatasetColumnDefinitionDisplay | Unset
        if isinstance(_display, Unset):
            display = UNSET
        else:
            display = DatasetColumnDefinitionDisplay.from_dict(_display)

        is_system = d.pop("is_system", UNSET)

        nullable = d.pop("nullable", UNSET)

        _provenance = d.pop("provenance", UNSET)
        provenance: DatasetColumnDefinitionProvenance | Unset
        if isinstance(_provenance, Unset):
            provenance = UNSET
        else:
            provenance = DatasetColumnDefinitionProvenance.from_dict(_provenance)

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        dataset_column_definition = cls(
            data_type=data_type,
            key=key,
            label=label,
            semantic_type=semantic_type,
            display=display,
            is_system=is_system,
            nullable=nullable,
            provenance=provenance,
            unit=unit,
        )

        return dataset_column_definition
