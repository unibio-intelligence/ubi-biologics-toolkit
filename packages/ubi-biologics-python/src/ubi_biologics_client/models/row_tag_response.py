from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.row_tag_response_assignment_source import RowTagResponseAssignmentSource
from ..models.tag_kind import TagKind

T = TypeVar("T", bound="RowTagResponse")


@_attrs_define
class RowTagResponse:
    """
    Attributes:
        assignment_source (RowTagResponseAssignmentSource):
        color (str):
        kind (TagKind):
        name (str):
        tag_id (str):
        tag_revision (int):
    """

    assignment_source: RowTagResponseAssignmentSource
    color: str
    kind: TagKind
    name: str
    tag_id: str
    tag_revision: int

    def to_dict(self) -> dict[str, Any]:
        assignment_source = self.assignment_source.value

        color = self.color

        kind = self.kind.value

        name = self.name

        tag_id = self.tag_id

        tag_revision = self.tag_revision

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "assignment_source": assignment_source,
                "color": color,
                "kind": kind,
                "name": name,
                "tag_id": tag_id,
                "tag_revision": tag_revision,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        assignment_source = RowTagResponseAssignmentSource(d.pop("assignment_source"))

        color = d.pop("color")

        kind = TagKind(d.pop("kind"))

        name = d.pop("name")

        tag_id = d.pop("tag_id")

        tag_revision = d.pop("tag_revision")

        row_tag_response = cls(
            assignment_source=assignment_source,
            color=color,
            kind=kind,
            name=name,
            tag_id=tag_id,
            tag_revision=tag_revision,
        )

        return row_tag_response
