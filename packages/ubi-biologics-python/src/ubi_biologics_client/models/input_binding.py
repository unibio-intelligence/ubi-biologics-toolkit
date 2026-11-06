from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.resource_kind import ResourceKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.input_binding_inline_value_type_0 import InputBindingInlineValueType0


T = TypeVar("T", bound="InputBinding")


@_attrs_define
class InputBinding:
    """
    Attributes:
        ordinal (int):
        resource_kind (ResourceKind):
        role (str):
        content_hash (None | str | Unset):
        inline_value (InputBindingInlineValueType0 | None | Unset):
        resource_id (None | str | Unset):
        resource_version_id (None | str | Unset):
        selection_id (None | str | Unset):
    """

    ordinal: int
    resource_kind: ResourceKind
    role: str
    content_hash: None | str | Unset = UNSET
    inline_value: InputBindingInlineValueType0 | None | Unset = UNSET
    resource_id: None | str | Unset = UNSET
    resource_version_id: None | str | Unset = UNSET
    selection_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.input_binding_inline_value_type_0 import (
            InputBindingInlineValueType0,
        )

        ordinal = self.ordinal

        resource_kind = self.resource_kind.value

        role = self.role

        content_hash: None | str | Unset
        if isinstance(self.content_hash, Unset):
            content_hash = UNSET
        else:
            content_hash = self.content_hash

        inline_value: dict[str, Any] | None | Unset
        if isinstance(self.inline_value, Unset):
            inline_value = UNSET
        elif isinstance(self.inline_value, InputBindingInlineValueType0):
            inline_value = self.inline_value.to_dict()
        else:
            inline_value = self.inline_value

        resource_id: None | str | Unset
        if isinstance(self.resource_id, Unset):
            resource_id = UNSET
        else:
            resource_id = self.resource_id

        resource_version_id: None | str | Unset
        if isinstance(self.resource_version_id, Unset):
            resource_version_id = UNSET
        else:
            resource_version_id = self.resource_version_id

        selection_id: None | str | Unset
        if isinstance(self.selection_id, Unset):
            selection_id = UNSET
        else:
            selection_id = self.selection_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "ordinal": ordinal,
                "resource_kind": resource_kind,
                "role": role,
            }
        )
        if content_hash is not UNSET:
            field_dict["content_hash"] = content_hash
        if inline_value is not UNSET:
            field_dict["inline_value"] = inline_value
        if resource_id is not UNSET:
            field_dict["resource_id"] = resource_id
        if resource_version_id is not UNSET:
            field_dict["resource_version_id"] = resource_version_id
        if selection_id is not UNSET:
            field_dict["selection_id"] = selection_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.input_binding_inline_value_type_0 import (
            InputBindingInlineValueType0,
        )

        d = dict(src_dict)
        ordinal = d.pop("ordinal")

        resource_kind = ResourceKind(d.pop("resource_kind"))

        role = d.pop("role")

        def _parse_content_hash(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        content_hash = _parse_content_hash(d.pop("content_hash", UNSET))

        def _parse_inline_value(
            data: object,
        ) -> InputBindingInlineValueType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                inline_value_type_0 = InputBindingInlineValueType0.from_dict(data)

                return inline_value_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(InputBindingInlineValueType0 | None | Unset, data)

        inline_value = _parse_inline_value(d.pop("inline_value", UNSET))

        def _parse_resource_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        resource_id = _parse_resource_id(d.pop("resource_id", UNSET))

        def _parse_resource_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        resource_version_id = _parse_resource_version_id(
            d.pop("resource_version_id", UNSET)
        )

        def _parse_selection_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        selection_id = _parse_selection_id(d.pop("selection_id", UNSET))

        input_binding = cls(
            ordinal=ordinal,
            resource_kind=resource_kind,
            role=role,
            content_hash=content_hash,
            inline_value=inline_value,
            resource_id=resource_id,
            resource_version_id=resource_version_id,
            selection_id=selection_id,
        )

        return input_binding
