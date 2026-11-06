from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_response_metadata import ArtifactResponseMetadata


T = TypeVar("T", bound="ArtifactResponse")


@_attrs_define
class ArtifactResponse:
    """
    Attributes:
        checksum_hex (str):
        created_at (str):
        created_by_principal_id (str):
        download_href (str):
        id (str):
        kind (str):
        media_type (str):
        metadata (ArtifactResponseMetadata):
        name (str):
        organization_id (str):
        project_id (str):
        size_bytes (int):
        asset_id (None | str | Unset):
        job_id (None | str | Unset):
        run_id (None | str | Unset):
    """

    checksum_hex: str
    created_at: str
    created_by_principal_id: str
    download_href: str
    id: str
    kind: str
    media_type: str
    metadata: ArtifactResponseMetadata
    name: str
    organization_id: str
    project_id: str
    size_bytes: int
    asset_id: None | str | Unset = UNSET
    job_id: None | str | Unset = UNSET
    run_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        checksum_hex = self.checksum_hex

        created_at = self.created_at

        created_by_principal_id = self.created_by_principal_id

        download_href = self.download_href

        id = self.id

        kind = self.kind

        media_type = self.media_type

        metadata = self.metadata.to_dict()

        name = self.name

        organization_id = self.organization_id

        project_id = self.project_id

        size_bytes = self.size_bytes

        asset_id: None | str | Unset
        if isinstance(self.asset_id, Unset):
            asset_id = UNSET
        else:
            asset_id = self.asset_id

        job_id: None | str | Unset
        if isinstance(self.job_id, Unset):
            job_id = UNSET
        else:
            job_id = self.job_id

        run_id: None | str | Unset
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        else:
            run_id = self.run_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "checksum_hex": checksum_hex,
                "created_at": created_at,
                "created_by_principal_id": created_by_principal_id,
                "download_href": download_href,
                "id": id,
                "kind": kind,
                "media_type": media_type,
                "metadata": metadata,
                "name": name,
                "organization_id": organization_id,
                "project_id": project_id,
                "size_bytes": size_bytes,
            }
        )
        if asset_id is not UNSET:
            field_dict["asset_id"] = asset_id
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if run_id is not UNSET:
            field_dict["run_id"] = run_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_response_metadata import ArtifactResponseMetadata

        d = dict(src_dict)
        checksum_hex = d.pop("checksum_hex")

        created_at = d.pop("created_at")

        created_by_principal_id = d.pop("created_by_principal_id")

        download_href = d.pop("download_href")

        id = d.pop("id")

        kind = d.pop("kind")

        media_type = d.pop("media_type")

        metadata = ArtifactResponseMetadata.from_dict(d.pop("metadata"))

        name = d.pop("name")

        organization_id = d.pop("organization_id")

        project_id = d.pop("project_id")

        size_bytes = d.pop("size_bytes")

        def _parse_asset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        asset_id = _parse_asset_id(d.pop("asset_id", UNSET))

        def _parse_job_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        job_id = _parse_job_id(d.pop("job_id", UNSET))

        def _parse_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        artifact_response = cls(
            checksum_hex=checksum_hex,
            created_at=created_at,
            created_by_principal_id=created_by_principal_id,
            download_href=download_href,
            id=id,
            kind=kind,
            media_type=media_type,
            metadata=metadata,
            name=name,
            organization_id=organization_id,
            project_id=project_id,
            size_bytes=size_bytes,
            asset_id=asset_id,
            job_id=job_id,
            run_id=run_id,
        )

        return artifact_response
