"""Reviewed, actionable errors safe across workers, MCP and CLI boundaries."""

import re
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any
from uuid import UUID, uuid4

from .error_catalog import MESSAGES

CORRELATION: ContextVar[str | None] = ContextVar("ubi_error_correlation", default=None)
RETRYABLE = frozenset(
    {
        "worker_capacity",
        "validation_capacity",
        "validation_unavailable",
        "deadline_exceeded",
        "dependency_unavailable",
        "upstream_capacity",
        "accounting_busy",
        "query_closing",
        "upload_timeout",
    }
)
INSPECT_REQUEST = frozenset(
    {
        "mutation_unknown",
        "request_unknown",
        "accounting_unresolved",
        "request_in_progress",
        "reservation_reconciled",
        "legacy_billing_review",
    }
)
DEFAULT_DELAY = {code: 1 for code in RETRYABLE if code != "deadline_exceeded"}
FIELD = re.compile(r"\$(?:\.[A-Za-z_][A-Za-z0-9_]{0,63}|\[\]){0,16}\Z")
FAILURE_REASONS = frozenset({"type_error", "attribute_error", "unexpected_failure"})


def uuid_value(value):
    if not isinstance(value, str) or len(value) > 64 or not value.isascii():
        return None
    try:
        return str(UUID(value))
    except ValueError:
        return None


@contextmanager
def error_scope():
    token = None
    if CORRELATION.get() is None:
        token = CORRELATION.set(str(uuid4()))
    try:
        yield CORRELATION.get()
    finally:
        if token is not None:
            CORRELATION.reset(token)


def safe_fields(values):
    if not isinstance(values, (list, tuple)):
        return []
    return list(
        dict.fromkeys(
            value
            for value in values[:8]
            if isinstance(value, str) and len(value) <= 256 and FIELD.fullmatch(value)
        )
    )


def recovery(code):
    if code in {"replay_expired", "request_not_found"}:
        return "operator_review"
    if code in {
        "agent_binding_unavailable",
        "agent_binding_invalid",
        "agent_grant_required",
        "agent_grant_expired",
        "agent_grant_budget_exhausted",
    }:
        return "operator_review"
    if code == "contract_review_required":
        return "operator_review"
    if code in INSPECT_REQUEST:
        return "inspect_request"
    if code in {"stale_preview"}:
        return "refresh_preview"
    if code in {"schema_drift", "invalid_operation_schema"}:
        return "refresh_schema"
    if code in {
        "unauthenticated",
        "expired_token",
        "login_required",
        "caller_token_required",
    }:
        return "reauthenticate"
    if code in RETRYABLE:
        return "retry_same_request"
    return "correct_request"


class ServiceError(Exception):
    def __init__(
        self,
        code: str,
        message: str | None = None,
        *,
        retryable: bool = False,
        request_key: str | None = None,
        correlation_id: str | None = None,
        field_paths=None,
        retry_after=None,
        operation=None,
        reason=None,
    ):
        # Messages and retry flags supplied by callers are never authoritative.
        # In particular, a downstream failure cannot enable mutation retries.
        self.code = (
            code if isinstance(code, str) and code in MESSAGES else "internal_error"
        )
        self.reason = (
            reason
            if isinstance(reason, str) and reason in FAILURE_REASONS
            else self.code
        )
        # Only owned registrations/reviewed operation names may cross this boundary.
        self.operation = None  # No private server operation registry in this client.
        super().__init__(MESSAGES[self.code])
        self.retryable = self.code in RETRYABLE
        # Only canonical request UUIDs are exposed; ledger keys may be opaque,
        # but echoing arbitrary submitted key text could disclose private data.
        self.request_key = (
            request_key
            if uuid_value(request_key) is not None
            and len(request_key) <= 64
            and request_key.isascii()
            else None
        )
        self.correlation_id = (
            uuid_value(correlation_id) or CORRELATION.get() or str(uuid4())
        )
        self.field_paths = safe_fields(field_paths)
        self.retry_after = (
            min(300, max(1, retry_after))
            if type(retry_after) is int and self.retryable
            else DEFAULT_DELAY.get(self.code)
        )

    def as_dict(self) -> dict[str, Any]:
        result = {
            "code": self.code,
            "message": str(self),
            "retryable": self.retryable,
            "correlation_id": self.correlation_id,
            "recovery": recovery(self.code),
            "reason": self.reason,
        }
        if self.operation is not None:
            result["operation"] = self.operation
        if self.request_key is not None:
            result["request_key"] = self.request_key
        if self.field_paths:
            result["field_paths"] = self.field_paths
        if self.retry_after is not None:
            result["retry_after_seconds"] = self.retry_after
        return result


def declared_path(parts, schema):
    """Only explicit schema properties; indexes and dynamic keys reveal no values."""
    field, current = "$", schema
    for part in list(parts)[:16]:
        properties = current.get("properties", {}) if isinstance(current, dict) else {}
        if (
            isinstance(part, str)
            and part in properties
            and part.isascii()
            and part.isidentifier()
            and len(part) <= 64
        ):
            field += "." + part
            current = properties[part]
        elif type(part) is int and isinstance(current, dict) and "items" in current:
            field += "[]"
            current = current["items"]
        else:
            break
    return field if len(field) <= 256 else "$"


def upstream_error(value, *, schema=None, preserve=False):
    if not isinstance(value, dict):
        return ServiceError("upstream_operation_failed")
    code = value.get("code")
    if not isinstance(code, str) or code not in MESSAGES:
        code = "upstream_operation_failed"
    fields = []
    if schema is not None:
        for field in safe_fields(value.get("field_paths")):
            parts = re.findall(r"\.([A-Za-z_][A-Za-z0-9_]*)|(\[\])", field)
            path = [name if name else 0 for name, _ in parts]
            if declared_path(path, schema) == field:
                fields.append(field)
    elif preserve:
        fields = safe_fields(value.get("field_paths"))
    return ServiceError(
        code,
        field_paths=fields,
        retry_after=value.get("retry_after_seconds"),
        correlation_id=value.get("correlation_id") if preserve else None,
        request_key=value.get("request_key") if preserve else None,
        operation=value.get("operation") if preserve else None,
        reason=value.get("reason") if preserve else None,
    )


def exception_error(error, *, fallback="internal_error"):
    """Classify by exception type/status; never copy diagnostic text or values."""
    if isinstance(error, ServiceError):
        return error
    if isinstance(error, PermissionError):
        return ServiceError("operation_denied")
    if isinstance(error, TimeoutError):
        return ServiceError("deadline_exceeded")
    if isinstance(error, ConnectionError):
        return ServiceError("dependency_unavailable")
    # Avoid importing optional database/HTTP drivers into every common consumer.
    cls = type(error)
    module, name = cls.__module__, cls.__name__
    if module.startswith("jsonschema."):
        return ServiceError(
            "schema_drift" if name == "ValidationError" else "invalid_operation_schema"
        )
    if module.startswith("pydantic"):
        return ServiceError("schema_drift")
    if module.startswith("fastmcp.") and name == "AuthorizationError":
        return ServiceError("operation_denied")
    if module == "_duckdb":
        code = {
            "ParserException": "invalid_sql",
            "BinderException": "schema_drift",
            "CatalogException": "schema_drift",
            "ConversionException": "invalid_query",
            "PermissionException": "operation_denied",
            "InterruptException": "deadline_exceeded",
            "OutOfMemoryException": "query_resource_limit",
            "IOException": "dependency_unavailable",
            "ConnectionException": "dependency_unavailable",
        }.get(name, "query_failed")
        return ServiceError(code)
    if module.startswith(("redis.", "httpx", "httpcore")):
        if "Timeout" in name:
            return ServiceError("deadline_exceeded")
        response = getattr(error, "response", None)
        status = getattr(response, "status_code", None)
        code = {
            400: "invalid_parameters",
            401: "unauthenticated",
            403: "operation_denied",
            404: "object_not_found",
            409: "conflict",
            429: "upstream_capacity",
        }.get(status, "dependency_unavailable")
        delay = None
        if status == 429:
            raw = response.headers.get("Retry-After", "")
            if (
                isinstance(raw, str)
                and len(raw) <= 3
                and raw.isascii()
                and raw.isdigit()
            ):
                delay = int(raw)
        return ServiceError(code, retry_after=delay)
    reason = (
        "type_error"
        if isinstance(error, TypeError)
        else "attribute_error"
        if isinstance(error, AttributeError)
        else "unexpected_failure"
    )
    return ServiceError(fallback, reason=reason)


def safe_error(error, *, fallback="internal_error"):
    # Frameworks can wrap safe exceptions in task groups or connection errors.
    pending, seen = [error], set()
    while pending and len(seen) < 32:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        if isinstance(current, ServiceError):
            return current
        if isinstance(current, BaseExceptionGroup):
            pending.extend(current.exceptions[:10])
        for nested in (current.__cause__, current.__context__):
            if nested is not None:
                pending.append(nested)
    pending, seen = [error], set()
    while pending and len(seen) < 32:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        mapped = exception_error(current, fallback=fallback)
        if mapped.code != fallback:
            return mapped
        if isinstance(current, BaseExceptionGroup):
            pending.extend(current.exceptions[:10])
        for nested in (current.__cause__, current.__context__):
            if nested is not None:
                pending.append(nested)
    return exception_error(error, fallback=fallback)
