from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.result_evidence_class import ResultEvidenceClass
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResultEvidenceEntryResponse")


@_attrs_define
class ResultEvidenceEntryResponse:
    """
    Attributes:
        applies_to (list[str]):
        caution (str):
        description (str):
        evidence_class (ResultEvidenceClass): Scientific truth boundary for a value shown in a result surface.
        id (str):
        label (str):
        method (str):
        provenance_requirements (list[str] | Unset):
    """

    applies_to: list[str]
    caution: str
    description: str
    evidence_class: ResultEvidenceClass
    id: str
    label: str
    method: str
    provenance_requirements: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        applies_to = self.applies_to

        caution = self.caution

        description = self.description

        evidence_class = self.evidence_class.value

        id = self.id

        label = self.label

        method = self.method

        provenance_requirements: list[str] | Unset = UNSET
        if not isinstance(self.provenance_requirements, Unset):
            provenance_requirements = self.provenance_requirements

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "applies_to": applies_to,
                "caution": caution,
                "description": description,
                "evidence_class": evidence_class,
                "id": id,
                "label": label,
                "method": method,
            }
        )
        if provenance_requirements is not UNSET:
            field_dict["provenance_requirements"] = provenance_requirements

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        applies_to = cast(list[str], d.pop("applies_to"))

        caution = d.pop("caution")

        description = d.pop("description")

        evidence_class = ResultEvidenceClass(d.pop("evidence_class"))

        id = d.pop("id")

        label = d.pop("label")

        method = d.pop("method")

        provenance_requirements = cast(
            list[str], d.pop("provenance_requirements", UNSET)
        )

        result_evidence_entry_response = cls(
            applies_to=applies_to,
            caution=caution,
            description=description,
            evidence_class=evidence_class,
            id=id,
            label=label,
            method=method,
            provenance_requirements=provenance_requirements,
        )

        return result_evidence_entry_response
