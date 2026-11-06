from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.dataset_kind import DatasetKind
from ..models.resource_kind import ResourceKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="CapabilityInputRoleResponse")


@_attrs_define
class CapabilityInputRoleResponse:
    """
    Attributes:
        resource_kinds (list[ResourceKind]):
        role (str):
        title (str):
        dataset_kinds (list[DatasetKind] | Unset):
        description (str | Unset):  Default: ''.
        granularity (list[str] | Unset):
        max_items (int | Unset):  Default: 1.
        media_types (list[str] | Unset):
        min_items (int | Unset):  Default: 1.
        ordered (bool | Unset):  Default: False.
        required (bool | Unset):  Default: True.
        required_fields (list[str] | Unset):
    """

    resource_kinds: list[ResourceKind]
    role: str
    title: str
    dataset_kinds: list[DatasetKind] | Unset = UNSET
    description: str | Unset = ""
    granularity: list[str] | Unset = UNSET
    max_items: int | Unset = 1
    media_types: list[str] | Unset = UNSET
    min_items: int | Unset = 1
    ordered: bool | Unset = False
    required: bool | Unset = True
    required_fields: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        resource_kinds = []
        for resource_kinds_item_data in self.resource_kinds:
            resource_kinds_item = resource_kinds_item_data.value
            resource_kinds.append(resource_kinds_item)

        role = self.role

        title = self.title

        dataset_kinds: list[str] | Unset = UNSET
        if not isinstance(self.dataset_kinds, Unset):
            dataset_kinds = []
            for dataset_kinds_item_data in self.dataset_kinds:
                dataset_kinds_item = dataset_kinds_item_data.value
                dataset_kinds.append(dataset_kinds_item)

        description = self.description

        granularity: list[str] | Unset = UNSET
        if not isinstance(self.granularity, Unset):
            granularity = self.granularity

        max_items = self.max_items

        media_types: list[str] | Unset = UNSET
        if not isinstance(self.media_types, Unset):
            media_types = self.media_types

        min_items = self.min_items

        ordered = self.ordered

        required = self.required

        required_fields: list[str] | Unset = UNSET
        if not isinstance(self.required_fields, Unset):
            required_fields = self.required_fields

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "resource_kinds": resource_kinds,
                "role": role,
                "title": title,
            }
        )
        if dataset_kinds is not UNSET:
            field_dict["dataset_kinds"] = dataset_kinds
        if description is not UNSET:
            field_dict["description"] = description
        if granularity is not UNSET:
            field_dict["granularity"] = granularity
        if max_items is not UNSET:
            field_dict["max_items"] = max_items
        if media_types is not UNSET:
            field_dict["media_types"] = media_types
        if min_items is not UNSET:
            field_dict["min_items"] = min_items
        if ordered is not UNSET:
            field_dict["ordered"] = ordered
        if required is not UNSET:
            field_dict["required"] = required
        if required_fields is not UNSET:
            field_dict["required_fields"] = required_fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_kinds = []
        _resource_kinds = d.pop("resource_kinds")
        for resource_kinds_item_data in _resource_kinds:
            resource_kinds_item = ResourceKind(resource_kinds_item_data)

            resource_kinds.append(resource_kinds_item)

        role = d.pop("role")

        title = d.pop("title")

        _dataset_kinds = d.pop("dataset_kinds", UNSET)
        dataset_kinds: list[DatasetKind] | Unset = UNSET
        if _dataset_kinds is not UNSET:
            dataset_kinds = []
            for dataset_kinds_item_data in _dataset_kinds:
                dataset_kinds_item = DatasetKind(dataset_kinds_item_data)

                dataset_kinds.append(dataset_kinds_item)

        description = d.pop("description", UNSET)

        granularity = cast(list[str], d.pop("granularity", UNSET))

        max_items = d.pop("max_items", UNSET)

        media_types = cast(list[str], d.pop("media_types", UNSET))

        min_items = d.pop("min_items", UNSET)

        ordered = d.pop("ordered", UNSET)

        required = d.pop("required", UNSET)

        required_fields = cast(list[str], d.pop("required_fields", UNSET))

        capability_input_role_response = cls(
            resource_kinds=resource_kinds,
            role=role,
            title=title,
            dataset_kinds=dataset_kinds,
            description=description,
            granularity=granularity,
            max_items=max_items,
            media_types=media_types,
            min_items=min_items,
            ordered=ordered,
            required=required,
            required_fields=required_fields,
        )

        return capability_input_role_response
