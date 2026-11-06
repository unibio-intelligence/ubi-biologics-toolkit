from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.artifact_response import ArtifactResponse
    from ..models.job_attempt_response import JobAttemptResponse
    from ..models.job_detail_response_lineage_item import JobDetailResponseLineageItem
    from ..models.job_list_item_response import JobListItemResponse
    from ..models.job_log_line_response import JobLogLineResponse
    from ..models.run_response import RunResponse


T = TypeVar("T", bound="JobDetailResponse")


@_attrs_define
class JobDetailResponse:
    """Complete authorized review context for one Job.

    Attributes:
        artifacts (list[ArtifactResponse]):
        attempts (list[JobAttemptResponse]):
        events (list[JobLogLineResponse]):
        job (JobListItemResponse): Bounded Job summary suitable for a global, permission-safe list.
        lineage (list[JobDetailResponseLineageItem]):
        log_download_href (str):
        run (RunResponse):
    """

    artifacts: list[ArtifactResponse]
    attempts: list[JobAttemptResponse]
    events: list[JobLogLineResponse]
    job: JobListItemResponse
    lineage: list[JobDetailResponseLineageItem]
    log_download_href: str
    run: RunResponse

    def to_dict(self) -> dict[str, Any]:
        artifacts = []
        for artifacts_item_data in self.artifacts:
            artifacts_item = artifacts_item_data.to_dict()
            artifacts.append(artifacts_item)

        attempts = []
        for attempts_item_data in self.attempts:
            attempts_item = attempts_item_data.to_dict()
            attempts.append(attempts_item)

        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()
            events.append(events_item)

        job = self.job.to_dict()

        lineage = []
        for lineage_item_data in self.lineage:
            lineage_item = lineage_item_data.to_dict()
            lineage.append(lineage_item)

        log_download_href = self.log_download_href

        run = self.run.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "artifacts": artifacts,
                "attempts": attempts,
                "events": events,
                "job": job,
                "lineage": lineage,
                "log_download_href": log_download_href,
                "run": run,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_response import ArtifactResponse
        from ..models.job_attempt_response import JobAttemptResponse
        from ..models.job_detail_response_lineage_item import (
            JobDetailResponseLineageItem,
        )
        from ..models.job_list_item_response import JobListItemResponse
        from ..models.job_log_line_response import JobLogLineResponse
        from ..models.run_response import RunResponse

        d = dict(src_dict)
        artifacts = []
        _artifacts = d.pop("artifacts")
        for artifacts_item_data in _artifacts:
            artifacts_item = ArtifactResponse.from_dict(artifacts_item_data)

            artifacts.append(artifacts_item)

        attempts = []
        _attempts = d.pop("attempts")
        for attempts_item_data in _attempts:
            attempts_item = JobAttemptResponse.from_dict(attempts_item_data)

            attempts.append(attempts_item)

        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = JobLogLineResponse.from_dict(events_item_data)

            events.append(events_item)

        job = JobListItemResponse.from_dict(d.pop("job"))

        lineage = []
        _lineage = d.pop("lineage")
        for lineage_item_data in _lineage:
            lineage_item = JobDetailResponseLineageItem.from_dict(lineage_item_data)

            lineage.append(lineage_item)

        log_download_href = d.pop("log_download_href")

        run = RunResponse.from_dict(d.pop("run"))

        job_detail_response = cls(
            artifacts=artifacts,
            attempts=attempts,
            events=events,
            job=job,
            lineage=lineage,
            log_download_href=log_download_href,
            run=run,
        )

        return job_detail_response
