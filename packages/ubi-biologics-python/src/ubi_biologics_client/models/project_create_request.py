from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.project_profile import ProjectProfile
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_create_request_settings import ProjectCreateRequestSettings


T = TypeVar("T", bound="ProjectCreateRequest")


@_attrs_define
class ProjectCreateRequest:
    """
    Attributes:
        name (str):
        description (str | Unset):  Default: ''.
        organization_id (None | str | Unset):
        profile (ProjectProfile | Unset):
        settings (ProjectCreateRequestSettings | Unset):
        tags (list[str] | Unset):
    """

    name: str
    description: str | Unset = ""
    organization_id: None | str | Unset = UNSET
    profile: ProjectProfile | Unset = UNSET
    settings: ProjectCreateRequestSettings | Unset = UNSET
    tags: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        organization_id: None | str | Unset
        if isinstance(self.organization_id, Unset):
            organization_id = UNSET
        else:
            organization_id = self.organization_id

        profile: str | Unset = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.value

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if profile is not UNSET:
            field_dict["profile"] = profile
        if settings is not UNSET:
            field_dict["settings"] = settings
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_create_request_settings import (
            ProjectCreateRequestSettings,
        )

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        def _parse_organization_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        organization_id = _parse_organization_id(d.pop("organization_id", UNSET))

        _profile = d.pop("profile", UNSET)
        profile: ProjectProfile | Unset
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = ProjectProfile(_profile)

        _settings = d.pop("settings", UNSET)
        settings: ProjectCreateRequestSettings | Unset
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = ProjectCreateRequestSettings.from_dict(_settings)

        tags = cast(list[str], d.pop("tags", UNSET))

        project_create_request = cls(
            name=name,
            description=description,
            organization_id=organization_id,
            profile=profile,
            settings=settings,
            tags=tags,
        )

        return project_create_request
