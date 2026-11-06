"""Bound JSON payloads before serialization and ledger retention."""

import json

from .errors import ServiceError

MAX_OUTPUT_BYTES = 4_000_000


def require_json_budget(value, *, max_bytes=MAX_OUTPUT_BYTES, max_cell_bytes=65536):
    pending = [(value, 0)]
    nodes = 0
    while pending:
        item, depth = pending.pop()
        nodes += 1
        if nodes > 100000 or depth > 32:
            raise ServiceError(
                "result_limit", "The result exceeds its JSON complexity budget."
            )
        if isinstance(item, str):
            if len(item) > max_cell_bytes or len(item.encode()) > max_cell_bytes:
                raise ServiceError(
                    "result_cell_limit", "A result cell exceeds its output budget."
                )
        elif isinstance(item, dict):
            pending.extend((key, depth + 1) for key in item)
            pending.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, (list, tuple)):
            pending.extend((child, depth + 1) for child in item)
    try:
        size = 0
        for chunk in json.JSONEncoder(allow_nan=False).iterencode(value):
            size += len(chunk.encode())
            if size > max_bytes:
                raise ServiceError(
                    "result_limit", "The result exceeds its total output budget."
                )
    except (ValueError, TypeError, OverflowError):
        raise ServiceError(
            "invalid_result", "The result is not finite JSON data."
        ) from None
    return value
