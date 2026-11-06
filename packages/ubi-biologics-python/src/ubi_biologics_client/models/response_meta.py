from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ResponseMeta")


@_attrs_define
class ResponseMeta:
    """
    Attributes:
        request_id (str):
        timestamp (datetime.datetime):
        trace_id (str):
    """

    request_id: str
    timestamp: datetime.datetime
    trace_id: str

    def to_dict(self) -> dict[str, Any]:
        request_id = self.request_id

        timestamp = self.timestamp.isoformat()

        trace_id = self.trace_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "request_id": request_id,
                "timestamp": timestamp,
                "trace_id": trace_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        request_id = d.pop("request_id")

        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))

        trace_id = d.pop("trace_id")

        response_meta = cls(
            request_id=request_id,
            timestamp=timestamp,
            trace_id=trace_id,
        )

        return response_meta
