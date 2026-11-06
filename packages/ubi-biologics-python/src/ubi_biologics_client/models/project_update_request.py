from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.project_profile import ProjectProfile
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_update_request_settings_type_0 import (
        ProjectUpdateRequestSettingsType0,
    )


T = TypeVar("T", bound="ProjectUpdateRequest")


@_attrs_define
class ProjectUpdateRequest:
    """
    Attributes:
        expected_revision (int):
        description (None | str | Unset):
        name (None | str | Unset):
        profile (None | ProjectProfile | Unset):
        settings (None | ProjectUpdateRequestSettingsType0 | Unset):
        tags (list[str] | None | Unset):
    """

    expected_revision: int
    description: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    profile: None | ProjectProfile | Unset = UNSET
    settings: None | ProjectUpdateRequestSettingsType0 | Unset = UNSET
    tags: list[str] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.project_update_request_settings_type_0 import (
            ProjectUpdateRequestSettingsType0,
        )

        expected_revision = self.expected_revision

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        profile: None | str | Unset
        if isinstance(self.profile, Unset):
            profile = UNSET
        elif isinstance(self.profile, ProjectProfile):
            profile = self.profile.value
        else:
            profile = self.profile

        settings: dict[str, Any] | None | Unset
        if isinstance(self.settings, Unset):
            settings = UNSET
        elif isinstance(self.settings, ProjectUpdateRequestSettingsType0):
            settings = self.settings.to_dict()
        else:
            settings = self.settings

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "expected_revision": expected_revision,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if profile is not UNSET:
            field_dict["profile"] = profile
        if settings is not UNSET:
            field_dict["settings"] = settings
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_update_request_settings_type_0 import (
            ProjectUpdateRequestSettingsType0,
        )

        d = dict(src_dict)
        expected_revision = d.pop("expected_revision")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_profile(data: object) -> None | ProjectProfile | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                profile_type_0 = ProjectProfile(data)

                return profile_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProjectProfile | Unset, data)

        profile = _parse_profile(d.pop("profile", UNSET))

        def _parse_settings(
            data: object,
        ) -> None | ProjectUpdateRequestSettingsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                settings_type_0 = ProjectUpdateRequestSettingsType0.from_dict(data)

                return settings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProjectUpdateRequestSettingsType0 | Unset, data)

        settings = _parse_settings(d.pop("settings", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        project_update_request = cls(
            expected_revision=expected_revision,
            description=description,
            name=name,
            profile=profile,
            settings=settings,
            tags=tags,
        )

        return project_update_request
