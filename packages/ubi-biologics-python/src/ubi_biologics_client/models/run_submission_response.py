from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.capability_output_response import CapabilityOutputResponse
    from ..models.fixed_credit_price_response import FixedCreditPriceResponse
    from ..models.job_response import JobResponse
    from ..models.run_response import RunResponse


T = TypeVar("T", bound="RunSubmissionResponse")


@_attrs_define
class RunSubmissionResponse:
    """
    Attributes:
        expected_outputs (list[CapabilityOutputResponse]):
        jobs (list[JobResponse]):
        pricing (FixedCreditPriceResponse): One simple, non-currency price known before a user action.
        run (RunResponse):
        status_href (str):
        workbench_href (str):
    """

    expected_outputs: list[CapabilityOutputResponse]
    jobs: list[JobResponse]
    pricing: FixedCreditPriceResponse
    run: RunResponse
    status_href: str
    workbench_href: str

    def to_dict(self) -> dict[str, Any]:
        expected_outputs = []
        for expected_outputs_item_data in self.expected_outputs:
            expected_outputs_item = expected_outputs_item_data.to_dict()
            expected_outputs.append(expected_outputs_item)

        jobs = []
        for jobs_item_data in self.jobs:
            jobs_item = jobs_item_data.to_dict()
            jobs.append(jobs_item)

        pricing = self.pricing.to_dict()

        run = self.run.to_dict()

        status_href = self.status_href

        workbench_href = self.workbench_href

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "expected_outputs": expected_outputs,
                "jobs": jobs,
                "pricing": pricing,
                "run": run,
                "status_href": status_href,
                "workbench_href": workbench_href,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.capability_output_response import CapabilityOutputResponse
        from ..models.fixed_credit_price_response import FixedCreditPriceResponse
        from ..models.job_response import JobResponse
        from ..models.run_response import RunResponse

        d = dict(src_dict)
        expected_outputs = []
        _expected_outputs = d.pop("expected_outputs")
        for expected_outputs_item_data in _expected_outputs:
            expected_outputs_item = CapabilityOutputResponse.from_dict(
                expected_outputs_item_data
            )

            expected_outputs.append(expected_outputs_item)

        jobs = []
        _jobs = d.pop("jobs")
        for jobs_item_data in _jobs:
            jobs_item = JobResponse.from_dict(jobs_item_data)

            jobs.append(jobs_item)

        pricing = FixedCreditPriceResponse.from_dict(d.pop("pricing"))

        run = RunResponse.from_dict(d.pop("run"))

        status_href = d.pop("status_href")

        workbench_href = d.pop("workbench_href")

        run_submission_response = cls(
            expected_outputs=expected_outputs,
            jobs=jobs,
            pricing=pricing,
            run=run,
            status_href=status_href,
            workbench_href=workbench_href,
        )

        return run_submission_response
