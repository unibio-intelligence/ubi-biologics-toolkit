from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.dataset_kind import DatasetKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_version_response import DatasetVersionResponse


T = TypeVar("T", bound="DatasetResponse")


@_attrs_define
class DatasetResponse:
    """
    Attributes:
        created_at (str):
        created_by_principal_id (str):
        current_version_id (str):
        id (str):
        kind (DatasetKind):
        name (str):
        organization_id (str):
        project_id (str):
        revision (int):
        status (str):
        updated_at (str):
        current_version (DatasetVersionResponse | None | Unset):
        folder_id (None | str | Unset):
    """

    created_at: str
    created_by_principal_id: str
    current_version_id: str
    id: str
    kind: DatasetKind
    name: str
    organization_id: str
    project_id: str
    revision: int
    status: str
    updated_at: str
    current_version: DatasetVersionResponse | None | Unset = UNSET
    folder_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_version_response import DatasetVersionResponse

        created_at = self.created_at

        created_by_principal_id = self.created_by_principal_id

        current_version_id = self.current_version_id

        id = self.id

        kind = self.kind.value

        name = self.name

        organization_id = self.organization_id

        project_id = self.project_id

        revision = self.revision

        status = self.status

        updated_at = self.updated_at

        current_version: dict[str, Any] | None | Unset
        if isinstance(self.current_version, Unset):
            current_version = UNSET
        elif isinstance(self.current_version, DatasetVersionResponse):
            current_version = self.current_version.to_dict()
        else:
            current_version = self.current_version

        folder_id: None | str | Unset
        if isinstance(self.folder_id, Unset):
            folder_id = UNSET
        else:
            folder_id = self.folder_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "created_at": created_at,
                "created_by_principal_id": created_by_principal_id,
                "current_version_id": current_version_id,
                "id": id,
                "kind": kind,
                "name": name,
                "organization_id": organization_id,
                "project_id": project_id,
                "revision": revision,
                "status": status,
                "updated_at": updated_at,
            }
        )
        if current_version is not UNSET:
            field_dict["current_version"] = current_version
        if folder_id is not UNSET:
            field_dict["folder_id"] = folder_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_version_response import DatasetVersionResponse

        d = dict(src_dict)
        created_at = d.pop("created_at")

        created_by_principal_id = d.pop("created_by_principal_id")

        current_version_id = d.pop("current_version_id")

        id = d.pop("id")

        kind = DatasetKind(d.pop("kind"))

        name = d.pop("name")

        organization_id = d.pop("organization_id")

        project_id = d.pop("project_id")

        revision = d.pop("revision")

        status = d.pop("status")

        updated_at = d.pop("updated_at")

        def _parse_current_version(
            data: object,
        ) -> DatasetVersionResponse | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                current_version_type_0 = DatasetVersionResponse.from_dict(data)

                return current_version_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DatasetVersionResponse | None | Unset, data)

        current_version = _parse_current_version(d.pop("current_version", UNSET))

        def _parse_folder_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        folder_id = _parse_folder_id(d.pop("folder_id", UNSET))

        dataset_response = cls(
            created_at=created_at,
            created_by_principal_id=created_by_principal_id,
            current_version_id=current_version_id,
            id=id,
            kind=kind,
            name=name,
            organization_id=organization_id,
            project_id=project_id,
            revision=revision,
            status=status,
            updated_at=updated_at,
            current_version=current_version,
            folder_id=folder_id,
        )

        return dataset_response
