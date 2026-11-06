from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.actor_type import ActorType
from ..models.principal_status import PrincipalStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="PrincipalResponse")


@_attrs_define
class PrincipalResponse:
    """
    Attributes:
        actor_type (ActorType):
        display_name (str):
        id (str):
        status (PrincipalStatus):
        human_user_id (None | str | Unset):
        on_behalf_of_principal_id (None | str | Unset):
        organization_id (None | str | Unset):
        responsible_principal_id (None | str | Unset):
        scopes (list[str] | Unset):
    """

    actor_type: ActorType
    display_name: str
    id: str
    status: PrincipalStatus
    human_user_id: None | str | Unset = UNSET
    on_behalf_of_principal_id: None | str | Unset = UNSET
    organization_id: None | str | Unset = UNSET
    responsible_principal_id: None | str | Unset = UNSET
    scopes: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        actor_type = self.actor_type.value

        display_name = self.display_name

        id = self.id

        status = self.status.value

        human_user_id: None | str | Unset
        if isinstance(self.human_user_id, Unset):
            human_user_id = UNSET
        else:
            human_user_id = self.human_user_id

        on_behalf_of_principal_id: None | str | Unset
        if isinstance(self.on_behalf_of_principal_id, Unset):
            on_behalf_of_principal_id = UNSET
        else:
            on_behalf_of_principal_id = self.on_behalf_of_principal_id

        organization_id: None | str | Unset
        if isinstance(self.organization_id, Unset):
            organization_id = UNSET
        else:
            organization_id = self.organization_id

        responsible_principal_id: None | str | Unset
        if isinstance(self.responsible_principal_id, Unset):
            responsible_principal_id = UNSET
        else:
            responsible_principal_id = self.responsible_principal_id

        scopes: list[str] | Unset = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "actor_type": actor_type,
                "display_name": display_name,
                "id": id,
                "status": status,
            }
        )
        if human_user_id is not UNSET:
            field_dict["human_user_id"] = human_user_id
        if on_behalf_of_principal_id is not UNSET:
            field_dict["on_behalf_of_principal_id"] = on_behalf_of_principal_id
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if responsible_principal_id is not UNSET:
            field_dict["responsible_principal_id"] = responsible_principal_id
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        actor_type = ActorType(d.pop("actor_type"))

        display_name = d.pop("display_name")

        id = d.pop("id")

        status = PrincipalStatus(d.pop("status"))

        def _parse_human_user_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        human_user_id = _parse_human_user_id(d.pop("human_user_id", UNSET))

        def _parse_on_behalf_of_principal_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        on_behalf_of_principal_id = _parse_on_behalf_of_principal_id(
            d.pop("on_behalf_of_principal_id", UNSET)
        )

        def _parse_organization_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        organization_id = _parse_organization_id(d.pop("organization_id", UNSET))

        def _parse_responsible_principal_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        responsible_principal_id = _parse_responsible_principal_id(
            d.pop("responsible_principal_id", UNSET)
        )

        scopes = cast(list[str], d.pop("scopes", UNSET))

        principal_response = cls(
            actor_type=actor_type,
            display_name=display_name,
            id=id,
            status=status,
            human_user_id=human_user_id,
            on_behalf_of_principal_id=on_behalf_of_principal_id,
            organization_id=organization_id,
            responsible_principal_id=responsible_principal_id,
            scopes=scopes,
        )

        return principal_response
