from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.dataset_kind import DatasetKind
from ..models.resource_kind import ResourceKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="CapabilityOutputResponse")


@_attrs_define
class CapabilityOutputResponse:
    """
    Attributes:
        resource_kind (ResourceKind):
        role (str):
        title (str):
        content_schema (None | str | Unset):
        dataset_kind (DatasetKind | None | Unset):
        description (str | Unset):  Default: ''.
        media_type (None | str | Unset):
    """

    resource_kind: ResourceKind
    role: str
    title: str
    content_schema: None | str | Unset = UNSET
    dataset_kind: DatasetKind | None | Unset = UNSET
    description: str | Unset = ""
    media_type: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        resource_kind = self.resource_kind.value

        role = self.role

        title = self.title

        content_schema: None | str | Unset
        if isinstance(self.content_schema, Unset):
            content_schema = UNSET
        else:
            content_schema = self.content_schema

        dataset_kind: None | str | Unset
        if isinstance(self.dataset_kind, Unset):
            dataset_kind = UNSET
        elif isinstance(self.dataset_kind, DatasetKind):
            dataset_kind = self.dataset_kind.value
        else:
            dataset_kind = self.dataset_kind

        description = self.description

        media_type: None | str | Unset
        if isinstance(self.media_type, Unset):
            media_type = UNSET
        else:
            media_type = self.media_type

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "resource_kind": resource_kind,
                "role": role,
                "title": title,
            }
        )
        if content_schema is not UNSET:
            field_dict["content_schema"] = content_schema
        if dataset_kind is not UNSET:
            field_dict["dataset_kind"] = dataset_kind
        if description is not UNSET:
            field_dict["description"] = description
        if media_type is not UNSET:
            field_dict["media_type"] = media_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_kind = ResourceKind(d.pop("resource_kind"))

        role = d.pop("role")

        title = d.pop("title")

        def _parse_content_schema(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        content_schema = _parse_content_schema(d.pop("content_schema", UNSET))

        def _parse_dataset_kind(data: object) -> DatasetKind | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                dataset_kind_type_0 = DatasetKind(data)

                return dataset_kind_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DatasetKind | None | Unset, data)

        dataset_kind = _parse_dataset_kind(d.pop("dataset_kind", UNSET))

        description = d.pop("description", UNSET)

        def _parse_media_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        media_type = _parse_media_type(d.pop("media_type", UNSET))

        capability_output_response = cls(
            resource_kind=resource_kind,
            role=role,
            title=title,
            content_schema=content_schema,
            dataset_kind=dataset_kind,
            description=description,
            media_type=media_type,
        )

        return capability_output_response
