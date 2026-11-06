from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.job_state import JobState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fixed_credit_price_response import FixedCreditPriceResponse
    from ..models.job_response_staged_outputs_item import JobResponseStagedOutputsItem


T = TypeVar("T", bound="JobResponse")


@_attrs_define
class JobResponse:
    """
    Attributes:
        attempt_count (int):
        cancellation_requested (bool):
        created_at (str):
        destination_project_id (str):
        id (str):
        max_attempts (int):
        pricing (FixedCreditPriceResponse): One simple, non-currency price known before a user action.
        publication_state (str):
        resource_class (str):
        run_id (str):
        staged_outputs (list[JobResponseStagedOutputsItem]):
        state (JobState):
        updated_at (str):
        completed_at (None | str | Unset):
    """

    attempt_count: int
    cancellation_requested: bool
    created_at: str
    destination_project_id: str
    id: str
    max_attempts: int
    pricing: FixedCreditPriceResponse
    publication_state: str
    resource_class: str
    run_id: str
    staged_outputs: list[JobResponseStagedOutputsItem]
    state: JobState
    updated_at: str
    completed_at: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        attempt_count = self.attempt_count

        cancellation_requested = self.cancellation_requested

        created_at = self.created_at

        destination_project_id = self.destination_project_id

        id = self.id

        max_attempts = self.max_attempts

        pricing = self.pricing.to_dict()

        publication_state = self.publication_state

        resource_class = self.resource_class

        run_id = self.run_id

        staged_outputs = []
        for staged_outputs_item_data in self.staged_outputs:
            staged_outputs_item = staged_outputs_item_data.to_dict()
            staged_outputs.append(staged_outputs_item)

        state = self.state.value

        updated_at = self.updated_at

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "attempt_count": attempt_count,
                "cancellation_requested": cancellation_requested,
                "created_at": created_at,
                "destination_project_id": destination_project_id,
                "id": id,
                "max_attempts": max_attempts,
                "pricing": pricing,
                "publication_state": publication_state,
                "resource_class": resource_class,
                "run_id": run_id,
                "staged_outputs": staged_outputs,
                "state": state,
                "updated_at": updated_at,
            }
        )
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fixed_credit_price_response import FixedCreditPriceResponse
        from ..models.job_response_staged_outputs_item import (
            JobResponseStagedOutputsItem,
        )

        d = dict(src_dict)
        attempt_count = d.pop("attempt_count")

        cancellation_requested = d.pop("cancellation_requested")

        created_at = d.pop("created_at")

        destination_project_id = d.pop("destination_project_id")

        id = d.pop("id")

        max_attempts = d.pop("max_attempts")

        pricing = FixedCreditPriceResponse.from_dict(d.pop("pricing"))

        publication_state = d.pop("publication_state")

        resource_class = d.pop("resource_class")

        run_id = d.pop("run_id")

        staged_outputs = []
        _staged_outputs = d.pop("staged_outputs")
        for staged_outputs_item_data in _staged_outputs:
            staged_outputs_item = JobResponseStagedOutputsItem.from_dict(
                staged_outputs_item_data
            )

            staged_outputs.append(staged_outputs_item)

        state = JobState(d.pop("state"))

        updated_at = d.pop("updated_at")

        def _parse_completed_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        job_response = cls(
            attempt_count=attempt_count,
            cancellation_requested=cancellation_requested,
            created_at=created_at,
            destination_project_id=destination_project_id,
            id=id,
            max_attempts=max_attempts,
            pricing=pricing,
            publication_state=publication_state,
            resource_class=resource_class,
            run_id=run_id,
            staged_outputs=staged_outputs,
            state=state,
            updated_at=updated_at,
            completed_at=completed_at,
        )

        return job_response
