from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.job_state import JobState
from ..models.run_state import RunState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fixed_credit_price_response import FixedCreditPriceResponse
    from ..models.job_list_item_response_failure_type_0 import (
        JobListItemResponseFailureType0,
    )
    from ..models.job_output_link import JobOutputLink


T = TypeVar("T", bound="JobListItemResponse")


@_attrs_define
class JobListItemResponse:
    """Bounded Job summary suitable for a global, permission-safe list.

    Attributes:
        artifact_count (int):
        attempt_count (int):
        can_cancel (bool):
        can_rerun (bool):
        can_retry (bool):
        cancellation_requested (bool):
        capability_id (str):
        capability_version (str):
        created_at (str):
        duration_seconds (float):
        href (str):
        id (str):
        initiating_principal_id (str):
        max_attempts (int):
        output_count (int):
        pricing (FixedCreditPriceResponse): One simple, non-currency price known before a user action.
        project_href (str):
        project_id (str):
        project_name (str):
        publication_state (str):
        resource_class (str):
        run_href (str):
        run_id (str):
        run_state (RunState):
        state (JobState):
        updated_at (str):
        workbench_href (str):
        agent_run_id (None | str | Unset):
        completed_at (None | str | Unset):
        eta_seconds (float | None | Unset):
        failure (JobListItemResponseFailureType0 | None | Unset):
        latest_event_sequence (int | None | Unset):
        latest_event_type (None | str | Unset):
        organization_id (None | str | Unset):
        output_links (list[JobOutputLink] | Unset):
        parent_run_id (None | str | Unset):
        progress_fraction (float | None | Unset):
    """

    artifact_count: int
    attempt_count: int
    can_cancel: bool
    can_rerun: bool
    can_retry: bool
    cancellation_requested: bool
    capability_id: str
    capability_version: str
    created_at: str
    duration_seconds: float
    href: str
    id: str
    initiating_principal_id: str
    max_attempts: int
    output_count: int
    pricing: FixedCreditPriceResponse
    project_href: str
    project_id: str
    project_name: str
    publication_state: str
    resource_class: str
    run_href: str
    run_id: str
    run_state: RunState
    state: JobState
    updated_at: str
    workbench_href: str
    agent_run_id: None | str | Unset = UNSET
    completed_at: None | str | Unset = UNSET
    eta_seconds: float | None | Unset = UNSET
    failure: JobListItemResponseFailureType0 | None | Unset = UNSET
    latest_event_sequence: int | None | Unset = UNSET
    latest_event_type: None | str | Unset = UNSET
    organization_id: None | str | Unset = UNSET
    output_links: list[JobOutputLink] | Unset = UNSET
    parent_run_id: None | str | Unset = UNSET
    progress_fraction: float | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_list_item_response_failure_type_0 import (
            JobListItemResponseFailureType0,
        )

        artifact_count = self.artifact_count

        attempt_count = self.attempt_count

        can_cancel = self.can_cancel

        can_rerun = self.can_rerun

        can_retry = self.can_retry

        cancellation_requested = self.cancellation_requested

        capability_id = self.capability_id

        capability_version = self.capability_version

        created_at = self.created_at

        duration_seconds = self.duration_seconds

        href = self.href

        id = self.id

        initiating_principal_id = self.initiating_principal_id

        max_attempts = self.max_attempts

        output_count = self.output_count

        pricing = self.pricing.to_dict()

        project_href = self.project_href

        project_id = self.project_id

        project_name = self.project_name

        publication_state = self.publication_state

        resource_class = self.resource_class

        run_href = self.run_href

        run_id = self.run_id

        run_state = self.run_state.value

        state = self.state.value

        updated_at = self.updated_at

        workbench_href = self.workbench_href

        agent_run_id: None | str | Unset
        if isinstance(self.agent_run_id, Unset):
            agent_run_id = UNSET
        else:
            agent_run_id = self.agent_run_id

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = self.completed_at

        eta_seconds: float | None | Unset
        if isinstance(self.eta_seconds, Unset):
            eta_seconds = UNSET
        else:
            eta_seconds = self.eta_seconds

        failure: dict[str, Any] | None | Unset
        if isinstance(self.failure, Unset):
            failure = UNSET
        elif isinstance(self.failure, JobListItemResponseFailureType0):
            failure = self.failure.to_dict()
        else:
            failure = self.failure

        latest_event_sequence: int | None | Unset
        if isinstance(self.latest_event_sequence, Unset):
            latest_event_sequence = UNSET
        else:
            latest_event_sequence = self.latest_event_sequence

        latest_event_type: None | str | Unset
        if isinstance(self.latest_event_type, Unset):
            latest_event_type = UNSET
        else:
            latest_event_type = self.latest_event_type

        organization_id: None | str | Unset
        if isinstance(self.organization_id, Unset):
            organization_id = UNSET
        else:
            organization_id = self.organization_id

        output_links: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.output_links, Unset):
            output_links = []
            for output_links_item_data in self.output_links:
                output_links_item = output_links_item_data.to_dict()
                output_links.append(output_links_item)

        parent_run_id: None | str | Unset
        if isinstance(self.parent_run_id, Unset):
            parent_run_id = UNSET
        else:
            parent_run_id = self.parent_run_id

        progress_fraction: float | None | Unset
        if isinstance(self.progress_fraction, Unset):
            progress_fraction = UNSET
        else:
            progress_fraction = self.progress_fraction

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "artifact_count": artifact_count,
                "attempt_count": attempt_count,
                "can_cancel": can_cancel,
                "can_rerun": can_rerun,
                "can_retry": can_retry,
                "cancellation_requested": cancellation_requested,
                "capability_id": capability_id,
                "capability_version": capability_version,
                "created_at": created_at,
                "duration_seconds": duration_seconds,
                "href": href,
                "id": id,
                "initiating_principal_id": initiating_principal_id,
                "max_attempts": max_attempts,
                "output_count": output_count,
                "pricing": pricing,
                "project_href": project_href,
                "project_id": project_id,
                "project_name": project_name,
                "publication_state": publication_state,
                "resource_class": resource_class,
                "run_href": run_href,
                "run_id": run_id,
                "run_state": run_state,
                "state": state,
                "updated_at": updated_at,
                "workbench_href": workbench_href,
            }
        )
        if agent_run_id is not UNSET:
            field_dict["agent_run_id"] = agent_run_id
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if eta_seconds is not UNSET:
            field_dict["eta_seconds"] = eta_seconds
        if failure is not UNSET:
            field_dict["failure"] = failure
        if latest_event_sequence is not UNSET:
            field_dict["latest_event_sequence"] = latest_event_sequence
        if latest_event_type is not UNSET:
            field_dict["latest_event_type"] = latest_event_type
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if output_links is not UNSET:
            field_dict["output_links"] = output_links
        if parent_run_id is not UNSET:
            field_dict["parent_run_id"] = parent_run_id
        if progress_fraction is not UNSET:
            field_dict["progress_fraction"] = progress_fraction

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fixed_credit_price_response import FixedCreditPriceResponse
        from ..models.job_list_item_response_failure_type_0 import (
            JobListItemResponseFailureType0,
        )
        from ..models.job_output_link import JobOutputLink

        d = dict(src_dict)
        artifact_count = d.pop("artifact_count")

        attempt_count = d.pop("attempt_count")

        can_cancel = d.pop("can_cancel")

        can_rerun = d.pop("can_rerun")

        can_retry = d.pop("can_retry")

        cancellation_requested = d.pop("cancellation_requested")

        capability_id = d.pop("capability_id")

        capability_version = d.pop("capability_version")

        created_at = d.pop("created_at")

        duration_seconds = d.pop("duration_seconds")

        href = d.pop("href")

        id = d.pop("id")

        initiating_principal_id = d.pop("initiating_principal_id")

        max_attempts = d.pop("max_attempts")

        output_count = d.pop("output_count")

        pricing = FixedCreditPriceResponse.from_dict(d.pop("pricing"))

        project_href = d.pop("project_href")

        project_id = d.pop("project_id")

        project_name = d.pop("project_name")

        publication_state = d.pop("publication_state")

        resource_class = d.pop("resource_class")

        run_href = d.pop("run_href")

        run_id = d.pop("run_id")

        run_state = RunState(d.pop("run_state"))

        state = JobState(d.pop("state"))

        updated_at = d.pop("updated_at")

        workbench_href = d.pop("workbench_href")

        def _parse_agent_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_run_id = _parse_agent_run_id(d.pop("agent_run_id", UNSET))

        def _parse_completed_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        def _parse_eta_seconds(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        eta_seconds = _parse_eta_seconds(d.pop("eta_seconds", UNSET))

        def _parse_failure(
            data: object,
        ) -> JobListItemResponseFailureType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                failure_type_0 = JobListItemResponseFailureType0.from_dict(data)

                return failure_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobListItemResponseFailureType0 | None | Unset, data)

        failure = _parse_failure(d.pop("failure", UNSET))

        def _parse_latest_event_sequence(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        latest_event_sequence = _parse_latest_event_sequence(
            d.pop("latest_event_sequence", UNSET)
        )

        def _parse_latest_event_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        latest_event_type = _parse_latest_event_type(d.pop("latest_event_type", UNSET))

        def _parse_organization_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        organization_id = _parse_organization_id(d.pop("organization_id", UNSET))

        _output_links = d.pop("output_links", UNSET)
        output_links: list[JobOutputLink] | Unset = UNSET
        if _output_links is not UNSET:
            output_links = []
            for output_links_item_data in _output_links:
                output_links_item = JobOutputLink.from_dict(output_links_item_data)

                output_links.append(output_links_item)

        def _parse_parent_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_run_id = _parse_parent_run_id(d.pop("parent_run_id", UNSET))

        def _parse_progress_fraction(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        progress_fraction = _parse_progress_fraction(d.pop("progress_fraction", UNSET))

        job_list_item_response = cls(
            artifact_count=artifact_count,
            attempt_count=attempt_count,
            can_cancel=can_cancel,
            can_rerun=can_rerun,
            can_retry=can_retry,
            cancellation_requested=cancellation_requested,
            capability_id=capability_id,
            capability_version=capability_version,
            created_at=created_at,
            duration_seconds=duration_seconds,
            href=href,
            id=id,
            initiating_principal_id=initiating_principal_id,
            max_attempts=max_attempts,
            output_count=output_count,
            pricing=pricing,
            project_href=project_href,
            project_id=project_id,
            project_name=project_name,
            publication_state=publication_state,
            resource_class=resource_class,
            run_href=run_href,
            run_id=run_id,
            run_state=run_state,
            state=state,
            updated_at=updated_at,
            workbench_href=workbench_href,
            agent_run_id=agent_run_id,
            completed_at=completed_at,
            eta_seconds=eta_seconds,
            failure=failure,
            latest_event_sequence=latest_event_sequence,
            latest_event_type=latest_event_type,
            organization_id=organization_id,
            output_links=output_links,
            parent_run_id=parent_run_id,
            progress_fraction=progress_fraction,
        )

        return job_list_item_response
