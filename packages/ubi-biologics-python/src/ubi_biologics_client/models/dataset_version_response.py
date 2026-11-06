from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_column_response import DatasetColumnResponse
    from ..models.dataset_version_response_publication_evidence import (
        DatasetVersionResponsePublicationEvidence,
    )
    from ..models.dataset_version_response_storage_manifest import (
        DatasetVersionResponseStorageManifest,
    )
    from ..models.dataset_version_response_summary_statistics import (
        DatasetVersionResponseSummaryStatistics,
    )


T = TypeVar("T", bound="DatasetVersionResponse")


@_attrs_define
class DatasetVersionResponse:
    """
    Attributes:
        columns (list[DatasetColumnResponse]):
        content_digest (str):
        created_at (str):
        created_by_principal_id (str):
        creation_reason (str):
        dataset_id (str):
        id (str):
        organization_id (str):
        project_id (str):
        published_at (str):
        row_count (int):
        schema_digest (str):
        storage_class (str):
        storage_manifest (DatasetVersionResponseStorageManifest):
        summary_statistics (DatasetVersionResponseSummaryStatistics):
        version_number (int):
        parent_version_id (None | str | Unset):
        publication_evidence (DatasetVersionResponsePublicationEvidence | Unset):
        run_id (None | str | Unset):
        source_asset_id (None | str | Unset):
    """

    columns: list[DatasetColumnResponse]
    content_digest: str
    created_at: str
    created_by_principal_id: str
    creation_reason: str
    dataset_id: str
    id: str
    organization_id: str
    project_id: str
    published_at: str
    row_count: int
    schema_digest: str
    storage_class: str
    storage_manifest: DatasetVersionResponseStorageManifest
    summary_statistics: DatasetVersionResponseSummaryStatistics
    version_number: int
    parent_version_id: None | str | Unset = UNSET
    publication_evidence: DatasetVersionResponsePublicationEvidence | Unset = UNSET
    run_id: None | str | Unset = UNSET
    source_asset_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        columns = []
        for columns_item_data in self.columns:
            columns_item = columns_item_data.to_dict()
            columns.append(columns_item)

        content_digest = self.content_digest

        created_at = self.created_at

        created_by_principal_id = self.created_by_principal_id

        creation_reason = self.creation_reason

        dataset_id = self.dataset_id

        id = self.id

        organization_id = self.organization_id

        project_id = self.project_id

        published_at = self.published_at

        row_count = self.row_count

        schema_digest = self.schema_digest

        storage_class = self.storage_class

        storage_manifest = self.storage_manifest.to_dict()

        summary_statistics = self.summary_statistics.to_dict()

        version_number = self.version_number

        parent_version_id: None | str | Unset
        if isinstance(self.parent_version_id, Unset):
            parent_version_id = UNSET
        else:
            parent_version_id = self.parent_version_id

        publication_evidence: dict[str, Any] | Unset = UNSET
        if not isinstance(self.publication_evidence, Unset):
            publication_evidence = self.publication_evidence.to_dict()

        run_id: None | str | Unset
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        else:
            run_id = self.run_id

        source_asset_id: None | str | Unset
        if isinstance(self.source_asset_id, Unset):
            source_asset_id = UNSET
        else:
            source_asset_id = self.source_asset_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "columns": columns,
                "content_digest": content_digest,
                "created_at": created_at,
                "created_by_principal_id": created_by_principal_id,
                "creation_reason": creation_reason,
                "dataset_id": dataset_id,
                "id": id,
                "organization_id": organization_id,
                "project_id": project_id,
                "published_at": published_at,
                "row_count": row_count,
                "schema_digest": schema_digest,
                "storage_class": storage_class,
                "storage_manifest": storage_manifest,
                "summary_statistics": summary_statistics,
                "version_number": version_number,
            }
        )
        if parent_version_id is not UNSET:
            field_dict["parent_version_id"] = parent_version_id
        if publication_evidence is not UNSET:
            field_dict["publication_evidence"] = publication_evidence
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
        if source_asset_id is not UNSET:
            field_dict["source_asset_id"] = source_asset_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_column_response import DatasetColumnResponse
        from ..models.dataset_version_response_publication_evidence import (
            DatasetVersionResponsePublicationEvidence,
        )
        from ..models.dataset_version_response_storage_manifest import (
            DatasetVersionResponseStorageManifest,
        )
        from ..models.dataset_version_response_summary_statistics import (
            DatasetVersionResponseSummaryStatistics,
        )

        d = dict(src_dict)
        columns = []
        _columns = d.pop("columns")
        for columns_item_data in _columns:
            columns_item = DatasetColumnResponse.from_dict(columns_item_data)

            columns.append(columns_item)

        content_digest = d.pop("content_digest")

        created_at = d.pop("created_at")

        created_by_principal_id = d.pop("created_by_principal_id")

        creation_reason = d.pop("creation_reason")

        dataset_id = d.pop("dataset_id")

        id = d.pop("id")

        organization_id = d.pop("organization_id")

        project_id = d.pop("project_id")

        published_at = d.pop("published_at")

        row_count = d.pop("row_count")

        schema_digest = d.pop("schema_digest")

        storage_class = d.pop("storage_class")

        storage_manifest = DatasetVersionResponseStorageManifest.from_dict(
            d.pop("storage_manifest")
        )

        summary_statistics = DatasetVersionResponseSummaryStatistics.from_dict(
            d.pop("summary_statistics")
        )

        version_number = d.pop("version_number")

        def _parse_parent_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_version_id = _parse_parent_version_id(d.pop("parent_version_id", UNSET))

        _publication_evidence = d.pop("publication_evidence", UNSET)
        publication_evidence: DatasetVersionResponsePublicationEvidence | Unset
        if isinstance(_publication_evidence, Unset):
            publication_evidence = UNSET
        else:
            publication_evidence = DatasetVersionResponsePublicationEvidence.from_dict(
                _publication_evidence
            )

        def _parse_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        def _parse_source_asset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_asset_id = _parse_source_asset_id(d.pop("source_asset_id", UNSET))

        dataset_version_response = cls(
            columns=columns,
            content_digest=content_digest,
            created_at=created_at,
            created_by_principal_id=created_by_principal_id,
            creation_reason=creation_reason,
            dataset_id=dataset_id,
            id=id,
            organization_id=organization_id,
            project_id=project_id,
            published_at=published_at,
            row_count=row_count,
            schema_digest=schema_digest,
            storage_class=storage_class,
            storage_manifest=storage_manifest,
            summary_statistics=summary_statistics,
            version_number=version_number,
            parent_version_id=parent_version_id,
            publication_evidence=publication_evidence,
            run_id=run_id,
            source_asset_id=source_asset_id,
        )

        return dataset_version_response
