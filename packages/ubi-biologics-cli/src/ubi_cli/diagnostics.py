"""Owned processes retain reviewed diagnostics, not dependency log payloads."""

import logging

import fastmcp

from .errors import ServiceError, error_scope, safe_error

# These libraries can log request URIs, SQL/DSN errors, returned private values,
# OAuth query strings or remote MCP notifications before our boundary handles
# the exception. Sanitize at LogRecord creation so every handler (including
# later-added exporters) receives the same safe record. Application logs remain
# responsible for using reviewed codes and correlation IDs.
FOREIGN_LOGGERS = (
    "fastmcp",
    "mcp",
    "httpx",
    "httpx2",
    "httpcore",
    "httpcore2",
    "psycopg",
    "redis",
    "uvicorn",
    "boto3",
    "botocore",
    "s3transfer",
    "urllib3",
)


def configure_safe_diagnostics():
    # FastMCP native spans retain raw resource URIs and exception strings at the
    # low-level protocol seam. Owned runtimes use reviewed correlation logging;
    # app-owned telemetry can still emit safe counters without FastMCP spans.
    fastmcp.settings.telemetry_mode = "off"
    previous = logging.getLogRecordFactory()
    if getattr(previous, "_ubi_safe_diagnostics", False):
        return

    def factory(*args, **kwargs):
        record = previous(*args, **kwargs)
        if any(
            record.name == name or record.name.startswith(name + ".")
            for name in FOREIGN_LOGGERS
        ):
            with error_scope():
                error = (
                    safe_error(record.exc_info[1])
                    if record.exc_info and record.exc_info[1] is not None
                    else ServiceError("dependency_unavailable")
                )
            record.msg = "Dependency diagnostic code=%s correlation_id=%s"
            record.args = (error.code, error.correlation_id)
            record.exc_info = None
            record.exc_text = None
            record.stack_info = None
        return record

    factory._ubi_safe_diagnostics = True
    logging.setLogRecordFactory(factory)
