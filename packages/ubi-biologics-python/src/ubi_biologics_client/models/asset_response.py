from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AssetResponse")


@_attrs_define
class AssetResponse:
    """
    Attributes:
        checksum_algorithm (str):
        checksum_hex (str):
        created_at (str):
        created_by_principal_id (str):
        download_href (str):
        id (str):
        media_type (str):
        name (str):
        organization_id (str):
        project_id (str):
        size_bytes (int):
        source_type (str):
        status (str):
        folder_id (None | str | Unset):
    """

    checksum_algorithm: str
    checksum_hex: str
    created_at: str
    created_by_principal_id: str
    download_href: str
    id: str
    media_type: str
    name: str
    organization_id: str
    project_id: str
    size_bytes: int
    source_type: str
    status: str
    folder_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        checksum_algorithm = self.checksum_algorithm

        checksum_hex = self.checksum_hex

        created_at = self.created_at

        created_by_principal_id = self.created_by_principal_id

        download_href = self.download_href

        id = self.id

        media_type = self.media_type

        name = self.name

        organization_id = self.organization_id

        project_id = self.project_id

        size_bytes = self.size_bytes

        source_type = self.source_type

        status = self.status

        folder_id: None | str | Unset
        if isinstance(self.folder_id, Unset):
            folder_id = UNSET
        else:
            folder_id = self.folder_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "checksum_algorithm": checksum_algorithm,
                "checksum_hex": checksum_hex,
                "created_at": created_at,
                "created_by_principal_id": created_by_principal_id,
                "download_href": download_href,
                "id": id,
                "media_type": media_type,
                "name": name,
                "organization_id": organization_id,
                "project_id": project_id,
                "size_bytes": size_bytes,
                "source_type": source_type,
                "status": status,
            }
        )
        if folder_id is not UNSET:
            field_dict["folder_id"] = folder_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checksum_algorithm = d.pop("checksum_algorithm")

        checksum_hex = d.pop("checksum_hex")

        created_at = d.pop("created_at")

        created_by_principal_id = d.pop("created_by_principal_id")

        download_href = d.pop("download_href")

        id = d.pop("id")

        media_type = d.pop("media_type")

        name = d.pop("name")

        organization_id = d.pop("organization_id")

        project_id = d.pop("project_id")

        size_bytes = d.pop("size_bytes")

        source_type = d.pop("source_type")

        status = d.pop("status")

        def _parse_folder_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        folder_id = _parse_folder_id(d.pop("folder_id", UNSET))

        asset_response = cls(
            checksum_algorithm=checksum_algorithm,
            checksum_hex=checksum_hex,
            created_at=created_at,
            created_by_principal_id=created_by_principal_id,
            download_href=download_href,
            id=id,
            media_type=media_type,
            name=name,
            organization_id=organization_id,
            project_id=project_id,
            size_bytes=size_bytes,
            source_type=source_type,
            status=status,
            folder_id=folder_id,
        )

        return asset_response
