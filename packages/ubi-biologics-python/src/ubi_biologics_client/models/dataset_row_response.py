from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_row_response_values import DatasetRowResponseValues
    from ..models.row_tag_response import RowTagResponse


T = TypeVar("T", bound="DatasetRowResponse")


@_attrs_define
class DatasetRowResponse:
    """
    Attributes:
        content_hash (str):
        logical_row_id (str):
        ordinal (int):
        values (DatasetRowResponseValues):
        tags (list[RowTagResponse] | Unset):
    """

    content_hash: str
    logical_row_id: str
    ordinal: int
    values: DatasetRowResponseValues
    tags: list[RowTagResponse] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        content_hash = self.content_hash

        logical_row_id = self.logical_row_id

        ordinal = self.ordinal

        values = self.values.to_dict()

        tags: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "content_hash": content_hash,
                "logical_row_id": logical_row_id,
                "ordinal": ordinal,
                "values": values,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_row_response_values import DatasetRowResponseValues
        from ..models.row_tag_response import RowTagResponse

        d = dict(src_dict)
        content_hash = d.pop("content_hash")

        logical_row_id = d.pop("logical_row_id")

        ordinal = d.pop("ordinal")

        values = DatasetRowResponseValues.from_dict(d.pop("values"))

        _tags = d.pop("tags", UNSET)
        tags: list[RowTagResponse] | Unset = UNSET
        if _tags is not UNSET:
            tags = []
            for tags_item_data in _tags:
                tags_item = RowTagResponse.from_dict(tags_item_data)

                tags.append(tags_item)

        dataset_row_response = cls(
            content_hash=content_hash,
            logical_row_id=logical_row_id,
            ordinal=ordinal,
            values=values,
            tags=tags,
        )

        return dataset_row_response
