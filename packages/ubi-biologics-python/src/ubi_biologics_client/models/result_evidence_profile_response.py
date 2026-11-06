from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.result_evidence_profile_response_profile_source import (
    ResultEvidenceProfileResponseProfileSource,
)

if TYPE_CHECKING:
    from ..models.result_evidence_class_definition_response import (
        ResultEvidenceClassDefinitionResponse,
    )
    from ..models.result_evidence_entry_response import ResultEvidenceEntryResponse


T = TypeVar("T", bound="ResultEvidenceProfileResponse")


@_attrs_define
class ResultEvidenceProfileResponse:
    """
    Attributes:
        capability_id (str):
        definitions (list[ResultEvidenceClassDefinitionResponse]):
        entries (list[ResultEvidenceEntryResponse]):
        experimental_value_policy (str):
        profile_digest_sha256 (str):
        profile_id (str):
        profile_source (ResultEvidenceProfileResponseProfileSource):
        schema_version (str):
        tool_id (str):
    """

    capability_id: str
    definitions: list[ResultEvidenceClassDefinitionResponse]
    entries: list[ResultEvidenceEntryResponse]
    experimental_value_policy: str
    profile_digest_sha256: str
    profile_id: str
    profile_source: ResultEvidenceProfileResponseProfileSource
    schema_version: str
    tool_id: str

    def to_dict(self) -> dict[str, Any]:
        capability_id = self.capability_id

        definitions = []
        for definitions_item_data in self.definitions:
            definitions_item = definitions_item_data.to_dict()
            definitions.append(definitions_item)

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        experimental_value_policy = self.experimental_value_policy

        profile_digest_sha256 = self.profile_digest_sha256

        profile_id = self.profile_id

        profile_source = self.profile_source.value

        schema_version = self.schema_version

        tool_id = self.tool_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "capability_id": capability_id,
                "definitions": definitions,
                "entries": entries,
                "experimental_value_policy": experimental_value_policy,
                "profile_digest_sha256": profile_digest_sha256,
                "profile_id": profile_id,
                "profile_source": profile_source,
                "schema_version": schema_version,
                "tool_id": tool_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.result_evidence_class_definition_response import (
            ResultEvidenceClassDefinitionResponse,
        )
        from ..models.result_evidence_entry_response import ResultEvidenceEntryResponse

        d = dict(src_dict)
        capability_id = d.pop("capability_id")

        definitions = []
        _definitions = d.pop("definitions")
        for definitions_item_data in _definitions:
            definitions_item = ResultEvidenceClassDefinitionResponse.from_dict(
                definitions_item_data
            )

            definitions.append(definitions_item)

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = ResultEvidenceEntryResponse.from_dict(entries_item_data)

            entries.append(entries_item)

        experimental_value_policy = d.pop("experimental_value_policy")

        profile_digest_sha256 = d.pop("profile_digest_sha256")

        profile_id = d.pop("profile_id")

        profile_source = ResultEvidenceProfileResponseProfileSource(
            d.pop("profile_source")
        )

        schema_version = d.pop("schema_version")

        tool_id = d.pop("tool_id")

        result_evidence_profile_response = cls(
            capability_id=capability_id,
            definitions=definitions,
            entries=entries,
            experimental_value_policy=experimental_value_policy,
            profile_digest_sha256=profile_digest_sha256,
            profile_id=profile_id,
            profile_source=profile_source,
            schema_version=schema_version,
            tool_id=tool_id,
        )

        return result_evidence_profile_response
