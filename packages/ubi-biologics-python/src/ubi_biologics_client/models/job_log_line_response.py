from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_log_line_response_data import JobLogLineResponseData


T = TypeVar("T", bound="JobLogLineResponse")


@_attrs_define
class JobLogLineResponse:
    """Redacted, ordered diagnostic line reconstructed from durable evidence.

    Attributes:
        event_type (str):
        level (str):
        message (str):
        sequence (int):
        source (str):
        timestamp (str):
        data (JobLogLineResponseData | Unset):
    """

    event_type: str
    level: str
    message: str
    sequence: int
    source: str
    timestamp: str
    data: JobLogLineResponseData | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        event_type = self.event_type

        level = self.level

        message = self.message

        sequence = self.sequence

        source = self.source

        timestamp = self.timestamp

        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "event_type": event_type,
                "level": level,
                "message": message,
                "sequence": sequence,
                "source": source,
                "timestamp": timestamp,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_log_line_response_data import JobLogLineResponseData

        d = dict(src_dict)
        event_type = d.pop("event_type")

        level = d.pop("level")

        message = d.pop("message")

        sequence = d.pop("sequence")

        source = d.pop("source")

        timestamp = d.pop("timestamp")

        _data = d.pop("data", UNSET)
        data: JobLogLineResponseData | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = JobLogLineResponseData.from_dict(_data)

        job_log_line_response = cls(
            event_type=event_type,
            level=level,
            message=message,
            sequence=sequence,
            source=source,
            timestamp=timestamp,
            data=data,
        )

        return job_log_line_response
