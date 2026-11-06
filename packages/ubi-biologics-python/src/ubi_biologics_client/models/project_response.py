from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.project_profile import ProjectProfile
from ..models.project_role import ProjectRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_response_purge_error_type_0 import (
        ProjectResponsePurgeErrorType0,
    )
    from ..models.project_response_settings import ProjectResponseSettings


T = TypeVar("T", bound="ProjectResponse")


@_attrs_define
class ProjectResponse:
    """
    Attributes:
        created_at (str):
        description (str):
        id (str):
        is_default (bool):
        is_favorite (bool):
        name (str):
        organization_id (str):
        owner_principal_id (str):
        personal_state_revision (int):
        profile (ProjectProfile):
        revision (int):
        role (ProjectRole):
        settings (ProjectResponseSettings):
        status (str):
        tags (list[str]):
        updated_at (str):
        archived_at (None | str | Unset):
        last_opened_at (None | str | Unset):
        purge_after (None | str | Unset):
        purge_completed_at (None | str | Unset):
        purge_error (None | ProjectResponsePurgeErrorType0 | Unset):
        purge_started_at (None | str | Unset):
        trashed_at (None | str | Unset):
        trashed_by_principal_id (None | str | Unset):
    """

    created_at: str
    description: str
    id: str
    is_default: bool
    is_favorite: bool
    name: str
    organization_id: str
    owner_principal_id: str
    personal_state_revision: int
    profile: ProjectProfile
    revision: int
    role: ProjectRole
    settings: ProjectResponseSettings
    status: str
    tags: list[str]
    updated_at: str
    archived_at: None | str | Unset = UNSET
    last_opened_at: None | str | Unset = UNSET
    purge_after: None | str | Unset = UNSET
    purge_completed_at: None | str | Unset = UNSET
    purge_error: None | ProjectResponsePurgeErrorType0 | Unset = UNSET
    purge_started_at: None | str | Unset = UNSET
    trashed_at: None | str | Unset = UNSET
    trashed_by_principal_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.project_response_purge_error_type_0 import (
            ProjectResponsePurgeErrorType0,
        )

        created_at = self.created_at

        description = self.description

        id = self.id

        is_default = self.is_default

        is_favorite = self.is_favorite

        name = self.name

        organization_id = self.organization_id

        owner_principal_id = self.owner_principal_id

        personal_state_revision = self.personal_state_revision

        profile = self.profile.value

        revision = self.revision

        role = self.role.value

        settings = self.settings.to_dict()

        status = self.status

        tags = self.tags

        updated_at = self.updated_at

        archived_at: None | str | Unset
        if isinstance(self.archived_at, Unset):
            archived_at = UNSET
        else:
            archived_at = self.archived_at

        last_opened_at: None | str | Unset
        if isinstance(self.last_opened_at, Unset):
            last_opened_at = UNSET
        else:
            last_opened_at = self.last_opened_at

        purge_after: None | str | Unset
        if isinstance(self.purge_after, Unset):
            purge_after = UNSET
        else:
            purge_after = self.purge_after

        purge_completed_at: None | str | Unset
        if isinstance(self.purge_completed_at, Unset):
            purge_completed_at = UNSET
        else:
            purge_completed_at = self.purge_completed_at

        purge_error: dict[str, Any] | None | Unset
        if isinstance(self.purge_error, Unset):
            purge_error = UNSET
        elif isinstance(self.purge_error, ProjectResponsePurgeErrorType0):
            purge_error = self.purge_error.to_dict()
        else:
            purge_error = self.purge_error

        purge_started_at: None | str | Unset
        if isinstance(self.purge_started_at, Unset):
            purge_started_at = UNSET
        else:
            purge_started_at = self.purge_started_at

        trashed_at: None | str | Unset
        if isinstance(self.trashed_at, Unset):
            trashed_at = UNSET
        else:
            trashed_at = self.trashed_at

        trashed_by_principal_id: None | str | Unset
        if isinstance(self.trashed_by_principal_id, Unset):
            trashed_by_principal_id = UNSET
        else:
            trashed_by_principal_id = self.trashed_by_principal_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "created_at": created_at,
                "description": description,
                "id": id,
                "is_default": is_default,
                "is_favorite": is_favorite,
                "name": name,
                "organization_id": organization_id,
                "owner_principal_id": owner_principal_id,
                "personal_state_revision": personal_state_revision,
                "profile": profile,
                "revision": revision,
                "role": role,
                "settings": settings,
                "status": status,
                "tags": tags,
                "updated_at": updated_at,
            }
        )
        if archived_at is not UNSET:
            field_dict["archived_at"] = archived_at
        if last_opened_at is not UNSET:
            field_dict["last_opened_at"] = last_opened_at
        if purge_after is not UNSET:
            field_dict["purge_after"] = purge_after
        if purge_completed_at is not UNSET:
            field_dict["purge_completed_at"] = purge_completed_at
        if purge_error is not UNSET:
            field_dict["purge_error"] = purge_error
        if purge_started_at is not UNSET:
            field_dict["purge_started_at"] = purge_started_at
        if trashed_at is not UNSET:
            field_dict["trashed_at"] = trashed_at
        if trashed_by_principal_id is not UNSET:
            field_dict["trashed_by_principal_id"] = trashed_by_principal_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_response_purge_error_type_0 import (
            ProjectResponsePurgeErrorType0,
        )
        from ..models.project_response_settings import ProjectResponseSettings

        d = dict(src_dict)
        created_at = d.pop("created_at")

        description = d.pop("description")

        id = d.pop("id")

        is_default = d.pop("is_default")

        is_favorite = d.pop("is_favorite")

        name = d.pop("name")

        organization_id = d.pop("organization_id")

        owner_principal_id = d.pop("owner_principal_id")

        personal_state_revision = d.pop("personal_state_revision")

        profile = ProjectProfile(d.pop("profile"))

        revision = d.pop("revision")

        role = ProjectRole(d.pop("role"))

        settings = ProjectResponseSettings.from_dict(d.pop("settings"))

        status = d.pop("status")

        tags = cast(list[str], d.pop("tags"))

        updated_at = d.pop("updated_at")

        def _parse_archived_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        archived_at = _parse_archived_at(d.pop("archived_at", UNSET))

        def _parse_last_opened_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_opened_at = _parse_last_opened_at(d.pop("last_opened_at", UNSET))

        def _parse_purge_after(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        purge_after = _parse_purge_after(d.pop("purge_after", UNSET))

        def _parse_purge_completed_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        purge_completed_at = _parse_purge_completed_at(
            d.pop("purge_completed_at", UNSET)
        )

        def _parse_purge_error(
            data: object,
        ) -> None | ProjectResponsePurgeErrorType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                purge_error_type_0 = ProjectResponsePurgeErrorType0.from_dict(data)

                return purge_error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProjectResponsePurgeErrorType0 | Unset, data)

        purge_error = _parse_purge_error(d.pop("purge_error", UNSET))

        def _parse_purge_started_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        purge_started_at = _parse_purge_started_at(d.pop("purge_started_at", UNSET))

        def _parse_trashed_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trashed_at = _parse_trashed_at(d.pop("trashed_at", UNSET))

        def _parse_trashed_by_principal_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trashed_by_principal_id = _parse_trashed_by_principal_id(
            d.pop("trashed_by_principal_id", UNSET)
        )

        project_response = cls(
            created_at=created_at,
            description=description,
            id=id,
            is_default=is_default,
            is_favorite=is_favorite,
            name=name,
            organization_id=organization_id,
            owner_principal_id=owner_principal_id,
            personal_state_revision=personal_state_revision,
            profile=profile,
            revision=revision,
            role=role,
            settings=settings,
            status=status,
            tags=tags,
            updated_at=updated_at,
            archived_at=archived_at,
            last_opened_at=last_opened_at,
            purge_after=purge_after,
            purge_completed_at=purge_completed_at,
            purge_error=purge_error,
            purge_started_at=purge_started_at,
            trashed_at=trashed_at,
            trashed_by_principal_id=trashed_by_principal_id,
        )

        return project_response
