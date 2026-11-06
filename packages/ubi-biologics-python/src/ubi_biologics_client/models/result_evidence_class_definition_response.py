from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.result_evidence_class import ResultEvidenceClass

T = TypeVar("T", bound="ResultEvidenceClassDefinitionResponse")


@_attrs_define
class ResultEvidenceClassDefinitionResponse:
    """
    Attributes:
        definition (str):
        evidence_class (ResultEvidenceClass): Scientific truth boundary for a value shown in a result surface.
        label (str):
    """

    definition: str
    evidence_class: ResultEvidenceClass
    label: str

    def to_dict(self) -> dict[str, Any]:
        definition = self.definition

        evidence_class = self.evidence_class.value

        label = self.label

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "definition": definition,
                "evidence_class": evidence_class,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        definition = d.pop("definition")

        evidence_class = ResultEvidenceClass(d.pop("evidence_class"))

        label = d.pop("label")

        result_evidence_class_definition_response = cls(
            definition=definition,
            evidence_class=evidence_class,
            label=label,
        )

        return result_evidence_class_definition_response
