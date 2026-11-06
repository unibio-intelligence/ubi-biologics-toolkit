"""Bounded remote MCP client and safe platform error decoding."""

import json
import logging

import mcp_types
from fastmcp import Client as SDKClient
from fastmcp.client.client import CallToolResult
from fastmcp.telemetry import suppress_fastmcp_telemetry
from mcp.shared.exceptions import MCPError

from .errors import ServiceError, safe_error, upstream_error
from .diagnostics import configure_safe_diagnostics
from .limits import MAX_OUTPUT_BYTES, require_json_budget


def protocol_error(error):
    if isinstance(error, MCPError):
        code = {
            mcp_types.REQUEST_TIMEOUT: "deadline_exceeded",
            mcp_types.CONNECTION_CLOSED: "dependency_unavailable",
            mcp_types.INVALID_PARAMS: "invalid_parameters",
            mcp_types.METHOD_NOT_FOUND: "unknown_operation",
        }.get(error.error.code)
        if code:
            return ServiceError(code)
        message = error.error.message
        if isinstance(message, str) and len(message.encode()) <= 4096:
            try:
                value = json.loads(message)
            except (ValueError, RecursionError):
                value = None
            if isinstance(value, dict) and isinstance(value.get("error"), dict):
                return upstream_error(value["error"], preserve=True)
    return safe_error(error, fallback="upstream_operation_failed")


def decode_result(result, *, preserve_service_error=True):
    def checked(value):
        require_json_budget(value)
        if isinstance(value, dict) and value.get("error"):
            raise upstream_error(value["error"], preserve=preserve_service_error)
        return value

    if result.is_error:
        for content in result.content:
            if content.type == "text" and len(content.text.encode()) <= 4096:
                try:
                    value = json.loads(content.text)
                except (ValueError, RecursionError):
                    continue
                if isinstance(value, dict) and value.get("error"):
                    raise upstream_error(value["error"], preserve=preserve_service_error)
        raise ServiceError("upstream_operation_failed")
    if result.structured_content is not None:
        return checked(result.structured_content)
    if isinstance(result.data, (dict, list)):
        return checked(result.data)
    text = "\n".join(c.text for c in result.content if c.type == "text")
    if len(text.encode()) > MAX_OUTPUT_BYTES:
        raise ServiceError("result_limit")
    try:
        return checked(json.loads(text))
    except (ValueError, RecursionError):
        return {"text": text[:50000], "truncated": len(text) > 50000}


async def discard_remote_log(_message):
    return None


class Client(SDKClient):
    """Remote consumer without foreign diagnostic text or SDK output parsing."""

    def __init__(self, *args, preserve_service_error=True, **kwargs):
        configure_safe_diagnostics()
        # SDK diagnostics and peer log notifications can contain private input.
        for name in ("fastmcp.client", "mcp.client", "httpx2", "httpcore2"):
            logging.getLogger(name).setLevel(logging.CRITICAL + 1)
        kwargs["log_handler"] = discard_remote_log
        # Allow the native OAuth callback's full 180-second window plus setup.
        kwargs.setdefault("timeout", 240)
        super().__init__(*args, **kwargs)
        self._known_tools = None

    async def __aenter__(self):
        with suppress_fastmcp_telemetry():
            try:
                return await super().__aenter__()
            except Exception as exc:
                raise protocol_error(exc) from None

    async def __aexit__(self, *args):
        with suppress_fastmcp_telemetry():
            return await super().__aexit__(*args)

    async def call_tool(self, name, arguments=None, *, timeout=None, raise_on_error=True, meta=None):
        with suppress_fastmcp_telemetry():
            try:
                if self._known_tools is None:
                    await self.list_tools()
                if name not in self._known_tools:
                    raise ServiceError("unknown_operation")
                # Use the typed protocol result without compiling a remote schema
                # or letting SDK parsing emit private output diagnostics.
                raw = await self._await_with_session_monitoring(
                    self.session.send_request(
                        mcp_types.CallToolRequest(
                            params=mcp_types.CallToolRequestParams(name=name, arguments=arguments or {}, _meta=meta)
                        ),
                        mcp_types.CallToolResult,
                        request_read_timeout_seconds=timeout,
                    )
                )
                if raw.result_type != "complete":
                    raise ServiceError("schema_drift")
                require_json_budget(raw.model_dump(mode="json"), max_cell_bytes=MAX_OUTPUT_BYTES)
                if raw.structured_content is not None:
                    require_json_budget(raw.structured_content)
                result = CallToolResult(content=raw.content, structured_content=raw.structured_content,
                                        meta=raw.meta, data=raw.structured_content, is_error=raw.is_error)
                if result.is_error and raise_on_error:
                    decode_result(result)
                return result
            except Exception as exc:
                raise protocol_error(exc) from None

    async def list_tools(self, *args, **kwargs):
        with suppress_fastmcp_telemetry():
            try:
                tools = await super().list_tools(*args, **kwargs)
                require_json_budget([t.model_dump(mode="json") for t in tools], max_cell_bytes=MAX_OUTPUT_BYTES)
                self._known_tools = {t.name for t in tools}
                return tools
            except Exception as exc:
                raise protocol_error(exc) from None

    async def read_resource(self, uri, **kwargs):
        with suppress_fastmcp_telemetry():
            try:
                result = await self._await_with_session_monitoring(self.session.read_resource(uri, **kwargs))
                require_json_budget(result.model_dump(mode="json"), max_cell_bytes=MAX_OUTPUT_BYTES)
                return result.contents
            except Exception as exc:
                raise protocol_error(exc) from None

    async def get_prompt(self, name, arguments=None, **kwargs):
        with suppress_fastmcp_telemetry():
            try:
                if not isinstance(arguments or {}, dict) or any(not isinstance(v, str) for v in (arguments or {}).values()):
                    raise ServiceError("invalid_parameters", field_paths=["$.arguments"])
                result = await self._await_with_session_monitoring(self.session.get_prompt(name, arguments or {}, **kwargs))
                require_json_budget(result.model_dump(mode="json"), max_cell_bytes=MAX_OUTPUT_BYTES)
                return result
            except Exception as exc:
                raise protocol_error(exc) from None
