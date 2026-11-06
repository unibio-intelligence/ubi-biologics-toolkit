from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="CapabilityExecutorResponse")


@_attrs_define
class CapabilityExecutorResponse:
    """Scientist-safe scheduling characteristics for a governed capability.

    Native service coordinates, protocol fields, and health contracts belong to
    the restricted runtime registry. They must never be serialized through the
    authenticated scientist contract.

        Attributes:
            expected_duration_seconds (int):
            max_attempts (int):
            mode (str):
            resource_class (str):
            retry_backoff_seconds (list[int]):
            supports_cancellation (bool):
            timeout_seconds (int):
    """

    expected_duration_seconds: int
    max_attempts: int
    mode: str
    resource_class: str
    retry_backoff_seconds: list[int]
    supports_cancellation: bool
    timeout_seconds: int

    def to_dict(self) -> dict[str, Any]:
        expected_duration_seconds = self.expected_duration_seconds

        max_attempts = self.max_attempts

        mode = self.mode

        resource_class = self.resource_class

        retry_backoff_seconds = self.retry_backoff_seconds

        supports_cancellation = self.supports_cancellation

        timeout_seconds = self.timeout_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "expected_duration_seconds": expected_duration_seconds,
                "max_attempts": max_attempts,
                "mode": mode,
                "resource_class": resource_class,
                "retry_backoff_seconds": retry_backoff_seconds,
                "supports_cancellation": supports_cancellation,
                "timeout_seconds": timeout_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expected_duration_seconds = d.pop("expected_duration_seconds")

        max_attempts = d.pop("max_attempts")

        mode = d.pop("mode")

        resource_class = d.pop("resource_class")

        retry_backoff_seconds = cast(list[int], d.pop("retry_backoff_seconds"))

        supports_cancellation = d.pop("supports_cancellation")

        timeout_seconds = d.pop("timeout_seconds")

        capability_executor_response = cls(
            expected_duration_seconds=expected_duration_seconds,
            max_attempts=max_attempts,
            mode=mode,
            resource_class=resource_class,
            retry_backoff_seconds=retry_backoff_seconds,
            supports_cancellation=supports_cancellation,
            timeout_seconds=timeout_seconds,
        )

        return capability_executor_response
