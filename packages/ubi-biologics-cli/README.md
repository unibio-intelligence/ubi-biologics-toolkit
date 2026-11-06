# Ubi Biologics CLI

Part of **Ubi Biologics Toolkit**, by **UniBio Intelligence**.
Requires Python 3.13+. Install the source candidate or downloaded wheel:

```bash
uv tool install --python 3.13 ./packages/ubi-biologics-cli
# Or: uv tool install --python 3.13 /path/to/ubi_biologics_cli-0.1.0a1-py3-none-any.whl
ubi-biologics-cli --help
ubi-biologics-cli login
ubi-biologics-cli status
ubi-biologics-cli doctor
ubi-biologics-cli capabilities
ubi-biologics-cli operations '{"capability":"tools","search":"job"}'
ubi-biologics-cli tools
ubi-biologics-cli quota
```

`login` uses the maintained native client identity, a loopback callback and the
OS credential store. `status` reports local credentials; `doctor` checks the
server connection. `logout` revokes and removes the saved grant. `revoke`
revokes saved tokens. `logout --forget-local` explicitly removes local credentials
when server revocation cannot be completed. No plaintext token cache or dynamic
client registration fallback is used.

OAuth login does not by itself grant product Project access. In the same Ubi
account, open https://biologics.unibiointelligence.com/agent-studio and create
an AI connection for client ID
`https://mcp.unibiointelligence.com/.well-known/ubi-cli-client.json` and service
`https://mcp.unibiointelligence.com/mcp`. Choose one existing Project, Read only,
only `platform_whoami` and `list_projects`, zero credits and a one-hour duration.
Remove the form's other default actions before saving. Inspect the saved card,
then run `ubi-biologics-cli platform_whoami` and `ubi-biologics-cli list_projects`.

If those reads return `agent_grant_required`, check the saved connection's
account, exact client ID and service. `doctor` checks transport/discovery and
can succeed before product consent. See the source release's
[connection guide](../../docs/connect-cli.md) for renewal and account alignment.

For headless automation, supply your bearer token through `UBI_MCP_TOKEN`.
Use `UBI_MCP_URL` or `--url` for another resource. HTTP is supported only for
loopback with `UBI_PROFILE=local`; this does not install a local platform server.
Custom client identities use `UBI_CLI_CLIENT_ID` or `UBI_CLI_CLIENT_METADATA_URL`
and `UBI_CLI_CALLBACK_PORT`, matching an explicitly approved server configuration.

Commands use the canonical platform tool names and one JSON object supplied
inline, as `@file.json`, or through stdin with `-`. Inputs are bounded to 1 MiB
of finite UTF-8 JSON. Discover an operation and read its schema before calling it:

```bash
ubi-biologics-cli query_data @read-request.json
ubi-biologics-cli preview_model_simulation @draft.json
# Review the returned preview, price and receipt before submitting:
# ubi-biologics-cli submit_model_simulation @approved-request.json
```

Call the named tools returned by `tools`; its entries include their exact input
schemas. The authorized remote catalog determines which tools are available.
Mutations use named preview, submit, cancel and evidence-import tools with the
exact server schema, permissions and idempotency key. The retired generic
`query`, `query_batch`, `action`, `preview_run` and `submit_run` commands are rejected.
`request_status` inspects a request with an uncertain outcome.
Never resubmit an uncertain mutation under a new key. MCP discovery is available
through `tools`, `resources`, `read-resource`, `prompts` and `get-prompt`.
Successful output is JSON; safe errors use stderr and a nonzero exit status.

This package contains a remote client and native client-side authentication.
It does not contain the platform gateway, authorization server, public database
adapters, billing/accounting or worker implementations. Hosted access requires
your account and may cost credits. Install this GitHub-distributed component
locally; PyPI uploads are disabled by package metadata.
