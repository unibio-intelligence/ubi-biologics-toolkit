from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.tag_filter_combinator import TagFilterCombinator
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetTagFilter")


@_attrs_define
class DatasetTagFilter:
    """
    Attributes:
        tag_ids (list[str]):
        combinator (TagFilterCombinator | Unset):
    """

    tag_ids: list[str]
    combinator: TagFilterCombinator | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        tag_ids = self.tag_ids

        combinator: str | Unset = UNSET
        if not isinstance(self.combinator, Unset):
            combinator = self.combinator.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "tag_ids": tag_ids,
            }
        )
        if combinator is not UNSET:
            field_dict["combinator"] = combinator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tag_ids = cast(list[str], d.pop("tag_ids"))

        _combinator = d.pop("combinator", UNSET)
        combinator: TagFilterCombinator | Unset
        if isinstance(_combinator, Unset):
            combinator = UNSET
        else:
            combinator = TagFilterCombinator(_combinator)

        dataset_tag_filter = cls(
            tag_ids=tag_ids,
            combinator=combinator,
        )

        return dataset_tag_filter
