from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.usage_plan import UsagePlan
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.credential_rate_limit_status import CredentialRateLimitStatus
    from ..models.principal_response import PrincipalResponse
    from ..models.project_response import ProjectResponse
    from ..models.usage_plan_limits_response import UsagePlanLimitsResponse
    from ..models.who_am_i_response_mcp_grant_type_0 import WhoAmIResponseMcpGrantType0


T = TypeVar("T", bound="WhoAmIResponse")


@_attrs_define
class WhoAmIResponse:
    """
    Attributes:
        authentication_method (str):
        effective_scopes (list[str]):
        principal (PrincipalResponse):
        usage_limits (UsagePlanLimitsResponse):
        usage_plan (UsagePlan): Small hosted-account plan vocabulary.
        authenticated_at (None | str | Unset):
        authentication_assurance_level (str | Unset):  Default: 'aal1'.
        authentication_methods (list[str] | Unset):
        credential_id (None | str | Unset):
        credential_rate_limit (CredentialRateLimitStatus | None | Unset):
        default_project (None | ProjectResponse | Unset):
        delegation_id (None | str | Unset):
        expires_at (None | str | Unset):
        mcp_grant (None | Unset | WhoAmIResponseMcpGrantType0):
        policy_version (str | Unset):  Default: '2026-07-16.1'.
        project_ids (list[str] | Unset):
        session_last_active_at (None | str | Unset):
        tool_ids (list[str] | Unset):
    """

    authentication_method: str
    effective_scopes: list[str]
    principal: PrincipalResponse
    usage_limits: UsagePlanLimitsResponse
    usage_plan: UsagePlan
    authenticated_at: None | str | Unset = UNSET
    authentication_assurance_level: str | Unset = "aal1"
    authentication_methods: list[str] | Unset = UNSET
    credential_id: None | str | Unset = UNSET
    credential_rate_limit: CredentialRateLimitStatus | None | Unset = UNSET
    default_project: None | ProjectResponse | Unset = UNSET
    delegation_id: None | str | Unset = UNSET
    expires_at: None | str | Unset = UNSET
    mcp_grant: None | Unset | WhoAmIResponseMcpGrantType0 = UNSET
    policy_version: str | Unset = "2026-07-16.1"
    project_ids: list[str] | Unset = UNSET
    session_last_active_at: None | str | Unset = UNSET
    tool_ids: list[str] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.credential_rate_limit_status import CredentialRateLimitStatus
        from ..models.project_response import ProjectResponse
        from ..models.who_am_i_response_mcp_grant_type_0 import (
            WhoAmIResponseMcpGrantType0,
        )

        authentication_method = self.authentication_method

        effective_scopes = self.effective_scopes

        principal = self.principal.to_dict()

        usage_limits = self.usage_limits.to_dict()

        usage_plan = self.usage_plan.value

        authenticated_at: None | str | Unset
        if isinstance(self.authenticated_at, Unset):
            authenticated_at = UNSET
        else:
            authenticated_at = self.authenticated_at

        authentication_assurance_level = self.authentication_assurance_level

        authentication_methods: list[str] | Unset = UNSET
        if not isinstance(self.authentication_methods, Unset):
            authentication_methods = self.authentication_methods

        credential_id: None | str | Unset
        if isinstance(self.credential_id, Unset):
            credential_id = UNSET
        else:
            credential_id = self.credential_id

        credential_rate_limit: dict[str, Any] | None | Unset
        if isinstance(self.credential_rate_limit, Unset):
            credential_rate_limit = UNSET
        elif isinstance(self.credential_rate_limit, CredentialRateLimitStatus):
            credential_rate_limit = self.credential_rate_limit.to_dict()
        else:
            credential_rate_limit = self.credential_rate_limit

        default_project: dict[str, Any] | None | Unset
        if isinstance(self.default_project, Unset):
            default_project = UNSET
        elif isinstance(self.default_project, ProjectResponse):
            default_project = self.default_project.to_dict()
        else:
            default_project = self.default_project

        delegation_id: None | str | Unset
        if isinstance(self.delegation_id, Unset):
            delegation_id = UNSET
        else:
            delegation_id = self.delegation_id

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = self.expires_at

        mcp_grant: dict[str, Any] | None | Unset
        if isinstance(self.mcp_grant, Unset):
            mcp_grant = UNSET
        elif isinstance(self.mcp_grant, WhoAmIResponseMcpGrantType0):
            mcp_grant = self.mcp_grant.to_dict()
        else:
            mcp_grant = self.mcp_grant

        policy_version = self.policy_version

        project_ids: list[str] | Unset = UNSET
        if not isinstance(self.project_ids, Unset):
            project_ids = self.project_ids

        session_last_active_at: None | str | Unset
        if isinstance(self.session_last_active_at, Unset):
            session_last_active_at = UNSET
        else:
            session_last_active_at = self.session_last_active_at

        tool_ids: list[str] | Unset = UNSET
        if not isinstance(self.tool_ids, Unset):
            tool_ids = self.tool_ids

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "authentication_method": authentication_method,
                "effective_scopes": effective_scopes,
                "principal": principal,
                "usage_limits": usage_limits,
                "usage_plan": usage_plan,
            }
        )
        if authenticated_at is not UNSET:
            field_dict["authenticated_at"] = authenticated_at
        if authentication_assurance_level is not UNSET:
            field_dict["authentication_assurance_level"] = (
                authentication_assurance_level
            )
        if authentication_methods is not UNSET:
            field_dict["authentication_methods"] = authentication_methods
        if credential_id is not UNSET:
            field_dict["credential_id"] = credential_id
        if credential_rate_limit is not UNSET:
            field_dict["credential_rate_limit"] = credential_rate_limit
        if default_project is not UNSET:
            field_dict["default_project"] = default_project
        if delegation_id is not UNSET:
            field_dict["delegation_id"] = delegation_id
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if mcp_grant is not UNSET:
            field_dict["mcp_grant"] = mcp_grant
        if policy_version is not UNSET:
            field_dict["policy_version"] = policy_version
        if project_ids is not UNSET:
            field_dict["project_ids"] = project_ids
        if session_last_active_at is not UNSET:
            field_dict["session_last_active_at"] = session_last_active_at
        if tool_ids is not UNSET:
            field_dict["tool_ids"] = tool_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.credential_rate_limit_status import CredentialRateLimitStatus
        from ..models.principal_response import PrincipalResponse
        from ..models.project_response import ProjectResponse
        from ..models.usage_plan_limits_response import UsagePlanLimitsResponse
        from ..models.who_am_i_response_mcp_grant_type_0 import (
            WhoAmIResponseMcpGrantType0,
        )

        d = dict(src_dict)
        authentication_method = d.pop("authentication_method")

        effective_scopes = cast(list[str], d.pop("effective_scopes"))

        principal = PrincipalResponse.from_dict(d.pop("principal"))

        usage_limits = UsagePlanLimitsResponse.from_dict(d.pop("usage_limits"))

        usage_plan = UsagePlan(d.pop("usage_plan"))

        def _parse_authenticated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        authenticated_at = _parse_authenticated_at(d.pop("authenticated_at", UNSET))

        authentication_assurance_level = d.pop("authentication_assurance_level", UNSET)

        authentication_methods = cast(list[str], d.pop("authentication_methods", UNSET))

        def _parse_credential_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        credential_id = _parse_credential_id(d.pop("credential_id", UNSET))

        def _parse_credential_rate_limit(
            data: object,
        ) -> CredentialRateLimitStatus | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                credential_rate_limit_type_0 = CredentialRateLimitStatus.from_dict(data)

                return credential_rate_limit_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CredentialRateLimitStatus | None | Unset, data)

        credential_rate_limit = _parse_credential_rate_limit(
            d.pop("credential_rate_limit", UNSET)
        )

        def _parse_default_project(data: object) -> None | ProjectResponse | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                default_project_type_0 = ProjectResponse.from_dict(data)

                return default_project_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProjectResponse | Unset, data)

        default_project = _parse_default_project(d.pop("default_project", UNSET))

        def _parse_delegation_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        delegation_id = _parse_delegation_id(d.pop("delegation_id", UNSET))

        def _parse_expires_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_mcp_grant(
            data: object,
        ) -> None | Unset | WhoAmIResponseMcpGrantType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mcp_grant_type_0 = WhoAmIResponseMcpGrantType0.from_dict(data)

                return mcp_grant_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | WhoAmIResponseMcpGrantType0, data)

        mcp_grant = _parse_mcp_grant(d.pop("mcp_grant", UNSET))

        policy_version = d.pop("policy_version", UNSET)

        project_ids = cast(list[str], d.pop("project_ids", UNSET))

        def _parse_session_last_active_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_last_active_at = _parse_session_last_active_at(
            d.pop("session_last_active_at", UNSET)
        )

        tool_ids = cast(list[str], d.pop("tool_ids", UNSET))

        who_am_i_response = cls(
            authentication_method=authentication_method,
            effective_scopes=effective_scopes,
            principal=principal,
            usage_limits=usage_limits,
            usage_plan=usage_plan,
            authenticated_at=authenticated_at,
            authentication_assurance_level=authentication_assurance_level,
            authentication_methods=authentication_methods,
            credential_id=credential_id,
            credential_rate_limit=credential_rate_limit,
            default_project=default_project,
            delegation_id=delegation_id,
            expires_at=expires_at,
            mcp_grant=mcp_grant,
            policy_version=policy_version,
            project_ids=project_ids,
            session_last_active_at=session_last_active_at,
            tool_ids=tool_ids,
        )

        return who_am_i_response
