from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="JobOutputLink")


@_attrs_define
class JobOutputLink:
    """One authorized navigation target derived from a published output manifest.

    Attributes:
        href (str):
        id (str):
        kind (str):
        label (str):
    """

    href: str
    id: str
    kind: str
    label: str

    def to_dict(self) -> dict[str, Any]:
        href = self.href

        id = self.id

        kind = self.kind

        label = self.label

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "href": href,
                "id": id,
                "kind": kind,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        href = d.pop("href")

        id = d.pop("id")

        kind = d.pop("kind")

        label = d.pop("label")

        job_output_link = cls(
            href=href,
            id=id,
            kind=kind,
            label=label,
        )

        return job_output_link
