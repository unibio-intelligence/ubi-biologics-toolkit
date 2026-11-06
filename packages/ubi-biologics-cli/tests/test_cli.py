import base64
import json
import sys

import pytest
from fastmcp import FastMCP

from ubi_cli import cli
from ubi_cli.errors import ServiceError
from ubi_cli.transport import Client, decode_result


@pytest.fixture
def platform(monkeypatch):
    server = FastMCP("canonical-platform-fixture")

    @server.tool()
    def capabilities() -> dict:
        return {"product": "Ubi", "capabilities": ["data", "tools", "modeling"]}

    @server.tool()
    def operations(capability: str, search: str = "", limit: int = 20, offset: int = 0) -> dict:
        return {"capability": capability, "operations": [], "search": search}

    @server.tool()
    def quota() -> dict:
        return {"remaining": 1}

    @server.tool()
    def query_data(sql: str) -> dict:
        if sql == "denied":
            return {"error": {"code": "operation_denied", "message": "synthetic-private-value"}}
        return {"data": {"sql": sql}}

    @server.resource("fixture://binary")
    def binary() -> bytes:
        return b"example binary content"

    monkeypatch.setenv("UBI_MCP_TOKEN", "synthetic-fixture-token")
    monkeypatch.setattr(cli, "StreamableHttpTransport", lambda *a, **kw: server)
    def in_memory_client(target, **kwargs):
        assert kwargs.pop("auth") == "synthetic-fixture-token"
        return Client(target, **kwargs)
    monkeypatch.setattr(cli, "Client", in_memory_client)
    return server


def test_canonical_commands_use_actual_mcp_transport(platform, monkeypatch, capsys):
    for operation, args, key in [
        ("capabilities", {}, "capabilities"),
        ("operations", {"capability": "modeling", "search": "scenario"}, "operations"),
        ("quota", {}, "remaining"),
        ("query_data", {"sql": "SELECT 1"}, "data"),
    ]:
        monkeypatch.setattr(sys, "argv", ["ubi-biologics-cli", operation, json.dumps(args)])
        cli.main()
        output = capsys.readouterr()
        assert key in json.loads(output.out) and output.err == ""


async def test_protocol_discovery_and_binary_resource(platform):
    tools = await cli.call("tools", {})
    assert {t["name"] for t in tools} == {"capabilities", "operations", "quota", "query_data"}
    result = await cli.call("read-resource", {"uri": "fixture://binary"})
    assert base64.b64decode(result[0]["blob"]) == b"example binary content"


def test_owned_error_is_nonzero_and_foreign_message_is_redacted(platform, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["ubi-biologics-cli", "query_data", json.dumps({"sql": "denied"})])
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert json.loads(output.err)["error"]["code"] == "operation_denied"
    assert "synthetic-private-value" not in output.err


@pytest.mark.parametrize("command", ["servers", "query", "query_batch", "action", "preview_run", "submit_run"])
def test_retired_gateway_command_is_not_accepted(monkeypatch, command):
    monkeypatch.setattr(sys, "argv", ["ubi-biologics-cli", command])
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code == 2


async def test_unknown_tool_is_safe(platform):
    with pytest.raises(ServiceError) as exc:
        await cli.call("list_servers", {})
    assert exc.value.code == "unknown_operation"


async def test_server_execution_error_is_safe():
    server = FastMCP("foreign-error", mask_error_details=True)
    @server.tool()
    def fails() -> dict:
        raise RuntimeError("synthetic-secret")
    async with Client(server) as client:
        result = await client.call_tool("fails", {}, raise_on_error=False)
        with pytest.raises(ServiceError) as exc:
            decode_result(result)
        assert exc.value.code == "upstream_operation_failed"
        assert "synthetic-secret" not in str(exc.value)


def test_json_exponent_overflow_is_rejected_before_transport():
    with pytest.raises(ServiceError) as exc:
        cli.read_arguments('{"value":1e999}')
    assert exc.value.code == "invalid_arguments"


async def test_login_checks_authenticated_discovery_without_optional_ping(monkeypatch):
    class DiscoveryClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def list_tools(self):
            return []

        async def ping(self):
            raise AssertionError("A deployment may omit optional MCP ping support")

    async def status(*args):
        return {"tokens_present": True}

    monkeypatch.delenv("UBI_MCP_TOKEN", raising=False)
    monkeypatch.setattr(cli, "SecureKeyringStore", lambda *args: object())
    monkeypatch.setattr(cli, "NativeOAuth", lambda *args, **kwargs: object())
    monkeypatch.setattr(cli, "StreamableHttpTransport", lambda *args, **kwargs: object())
    monkeypatch.setattr(cli, "Client", lambda *args, **kwargs: DiscoveryClient())
    monkeypatch.setattr(cli, "credential_status", status)
    result = await cli.call("login", {})
    assert result == {"tokens_present": True, "server_authorization_checked": True}
