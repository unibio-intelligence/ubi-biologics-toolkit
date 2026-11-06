from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.error_category import ErrorCategory
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_body_details import ErrorBodyDetails
    from ..models.error_body_remediation_type_0 import ErrorBodyRemediationType0


T = TypeVar("T", bound="ErrorBody")


@_attrs_define
class ErrorBody:
    """
    Attributes:
        category (ErrorCategory): Stable machine-actionable error classes across every platform client.
        code (str):
        message (str):
        request_id (str):
        retryable (bool):
        timestamp (datetime.datetime):
        trace_id (str):
        details (ErrorBodyDetails | Unset):
        remediation (ErrorBodyRemediationType0 | None | Unset):
    """

    category: ErrorCategory
    code: str
    message: str
    request_id: str
    retryable: bool
    timestamp: datetime.datetime
    trace_id: str
    details: ErrorBodyDetails | Unset = UNSET
    remediation: ErrorBodyRemediationType0 | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.error_body_remediation_type_0 import ErrorBodyRemediationType0

        category = self.category.value

        code = self.code

        message = self.message

        request_id = self.request_id

        retryable = self.retryable

        timestamp = self.timestamp.isoformat()

        trace_id = self.trace_id

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        remediation: dict[str, Any] | None | Unset
        if isinstance(self.remediation, Unset):
            remediation = UNSET
        elif isinstance(self.remediation, ErrorBodyRemediationType0):
            remediation = self.remediation.to_dict()
        else:
            remediation = self.remediation

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "category": category,
                "code": code,
                "message": message,
                "request_id": request_id,
                "retryable": retryable,
                "timestamp": timestamp,
                "trace_id": trace_id,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details
        if remediation is not UNSET:
            field_dict["remediation"] = remediation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_body_details import ErrorBodyDetails
        from ..models.error_body_remediation_type_0 import ErrorBodyRemediationType0

        d = dict(src_dict)
        category = ErrorCategory(d.pop("category"))

        code = d.pop("code")

        message = d.pop("message")

        request_id = d.pop("request_id")

        retryable = d.pop("retryable")

        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))

        trace_id = d.pop("trace_id")

        _details = d.pop("details", UNSET)
        details: ErrorBodyDetails | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = ErrorBodyDetails.from_dict(_details)

        def _parse_remediation(
            data: object,
        ) -> ErrorBodyRemediationType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                remediation_type_0 = ErrorBodyRemediationType0.from_dict(data)

                return remediation_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ErrorBodyRemediationType0 | None | Unset, data)

        remediation = _parse_remediation(d.pop("remediation", UNSET))

        error_body = cls(
            category=category,
            code=code,
            message=message,
            request_id=request_id,
            retryable=retryable,
            timestamp=timestamp,
            trace_id=trace_id,
            details=details,
            remediation=remediation,
        )

        return error_body
