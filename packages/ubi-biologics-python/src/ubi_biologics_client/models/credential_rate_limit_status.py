from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CredentialRateLimitStatus")


@_attrs_define
class CredentialRateLimitStatus:
    """
    Attributes:
        remaining (int):
        reset_at (str):
        request_limit (int | Unset):  Default: 600.
        window_seconds (int | Unset):  Default: 60.
    """

    remaining: int
    reset_at: str
    request_limit: int | Unset = 600
    window_seconds: int | Unset = 60

    def to_dict(self) -> dict[str, Any]:
        remaining = self.remaining

        reset_at = self.reset_at

        request_limit = self.request_limit

        window_seconds = self.window_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "remaining": remaining,
                "reset_at": reset_at,
            }
        )
        if request_limit is not UNSET:
            field_dict["request_limit"] = request_limit
        if window_seconds is not UNSET:
            field_dict["window_seconds"] = window_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        remaining = d.pop("remaining")

        reset_at = d.pop("reset_at")

        request_limit = d.pop("request_limit", UNSET)

        window_seconds = d.pop("window_seconds", UNSET)

        credential_rate_limit_status = cls(
            remaining=remaining,
            reset_at=reset_at,
            request_limit=request_limit,
            window_seconds=window_seconds,
        )

        return credential_rate_limit_status
