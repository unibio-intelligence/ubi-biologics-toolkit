from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.job_event_response_data import JobEventResponseData


T = TypeVar("T", bound="JobEventResponse")


@_attrs_define
class JobEventResponse:
    """
    Attributes:
        created_at (str):
        data (JobEventResponseData):
        event_type (str):
        id (str):
        job_id (str):
        sequence (int):
    """

    created_at: str
    data: JobEventResponseData
    event_type: str
    id: str
    job_id: str
    sequence: int

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        data = self.data.to_dict()

        event_type = self.event_type

        id = self.id

        job_id = self.job_id

        sequence = self.sequence

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "created_at": created_at,
                "data": data,
                "event_type": event_type,
                "id": id,
                "job_id": job_id,
                "sequence": sequence,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_event_response_data import JobEventResponseData

        d = dict(src_dict)
        created_at = d.pop("created_at")

        data = JobEventResponseData.from_dict(d.pop("data"))

        event_type = d.pop("event_type")

        id = d.pop("id")

        job_id = d.pop("job_id")

        sequence = d.pop("sequence")

        job_event_response = cls(
            created_at=created_at,
            data=data,
            event_type=event_type,
            id=id,
            job_id=job_id,
            sequence=sequence,
        )

        return job_event_response
