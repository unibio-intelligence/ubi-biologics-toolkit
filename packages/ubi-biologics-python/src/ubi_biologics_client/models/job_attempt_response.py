from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.job_attempt_state import JobAttemptState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_attempt_response_error_type_0 import JobAttemptResponseErrorType0
    from ..models.job_attempt_response_resource_usage import (
        JobAttemptResponseResourceUsage,
    )


T = TypeVar("T", bound="JobAttemptResponse")


@_attrs_define
class JobAttemptResponse:
    """Immutable worker Attempt evidence without lease credentials.

    Attributes:
        attempt_number (int):
        created_at (str):
        duration_seconds (float):
        id (str):
        job_id (str):
        lease_expires_at (str):
        state (JobAttemptState):
        worker_id (str):
        completed_at (None | str | Unset):
        error (JobAttemptResponseErrorType0 | None | Unset):
        heartbeat_at (None | str | Unset):
        native_execution_reference (None | str | Unset):
        resource_usage (JobAttemptResponseResourceUsage | Unset):
        started_at (None | str | Unset):
    """

    attempt_number: int
    created_at: str
    duration_seconds: float
    id: str
    job_id: str
    lease_expires_at: str
    state: JobAttemptState
    worker_id: str
    completed_at: None | str | Unset = UNSET
    error: JobAttemptResponseErrorType0 | None | Unset = UNSET
    heartbeat_at: None | str | Unset = UNSET
    native_execution_reference: None | str | Unset = UNSET
    resource_usage: JobAttemptResponseResourceUsage | Unset = UNSET
    started_at: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_attempt_response_error_type_0 import (
            JobAttemptResponseErrorType0,
        )

        attempt_number = self.attempt_number

        created_at = self.created_at

        duration_seconds = self.duration_seconds

        id = self.id

        job_id = self.job_id

        lease_expires_at = self.lease_expires_at

        state = self.state.value

        worker_id = self.worker_id

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = self.completed_at

        error: dict[str, Any] | None | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        elif isinstance(self.error, JobAttemptResponseErrorType0):
            error = self.error.to_dict()
        else:
            error = self.error

        heartbeat_at: None | str | Unset
        if isinstance(self.heartbeat_at, Unset):
            heartbeat_at = UNSET
        else:
            heartbeat_at = self.heartbeat_at

        native_execution_reference: None | str | Unset
        if isinstance(self.native_execution_reference, Unset):
            native_execution_reference = UNSET
        else:
            native_execution_reference = self.native_execution_reference

        resource_usage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.resource_usage, Unset):
            resource_usage = self.resource_usage.to_dict()

        started_at: None | str | Unset
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        else:
            started_at = self.started_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "attempt_number": attempt_number,
                "created_at": created_at,
                "duration_seconds": duration_seconds,
                "id": id,
                "job_id": job_id,
                "lease_expires_at": lease_expires_at,
                "state": state,
                "worker_id": worker_id,
            }
        )
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if error is not UNSET:
            field_dict["error"] = error
        if heartbeat_at is not UNSET:
            field_dict["heartbeat_at"] = heartbeat_at
        if native_execution_reference is not UNSET:
            field_dict["native_execution_reference"] = native_execution_reference
        if resource_usage is not UNSET:
            field_dict["resource_usage"] = resource_usage
        if started_at is not UNSET:
            field_dict["started_at"] = started_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_attempt_response_error_type_0 import (
            JobAttemptResponseErrorType0,
        )
        from ..models.job_attempt_response_resource_usage import (
            JobAttemptResponseResourceUsage,
        )

        d = dict(src_dict)
        attempt_number = d.pop("attempt_number")

        created_at = d.pop("created_at")

        duration_seconds = d.pop("duration_seconds")

        id = d.pop("id")

        job_id = d.pop("job_id")

        lease_expires_at = d.pop("lease_expires_at")

        state = JobAttemptState(d.pop("state"))

        worker_id = d.pop("worker_id")

        def _parse_completed_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        def _parse_error(data: object) -> JobAttemptResponseErrorType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = JobAttemptResponseErrorType0.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobAttemptResponseErrorType0 | None | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_heartbeat_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        heartbeat_at = _parse_heartbeat_at(d.pop("heartbeat_at", UNSET))

        def _parse_native_execution_reference(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        native_execution_reference = _parse_native_execution_reference(
            d.pop("native_execution_reference", UNSET)
        )

        _resource_usage = d.pop("resource_usage", UNSET)
        resource_usage: JobAttemptResponseResourceUsage | Unset
        if isinstance(_resource_usage, Unset):
            resource_usage = UNSET
        else:
            resource_usage = JobAttemptResponseResourceUsage.from_dict(_resource_usage)

        def _parse_started_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        started_at = _parse_started_at(d.pop("started_at", UNSET))

        job_attempt_response = cls(
            attempt_number=attempt_number,
            created_at=created_at,
            duration_seconds=duration_seconds,
            id=id,
            job_id=job_id,
            lease_expires_at=lease_expires_at,
            state=state,
            worker_id=worker_id,
            completed_at=completed_at,
            error=error,
            heartbeat_at=heartbeat_at,
            native_execution_reference=native_execution_reference,
            resource_usage=resource_usage,
            started_at=started_at,
        )

        return job_attempt_response
