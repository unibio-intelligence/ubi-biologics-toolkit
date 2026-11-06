# Connect the CLI to your Project

CLI login and Project access are separate steps. `doctor` can pass while product
reads still require an AI connection. Use the same Ubi account in the CLI's
browser login and in the Project settings below.

## Sign in

```bash
ubi-biologics-cli login
ubi-biologics-cli status
ubi-biologics-cli doctor
```

Finish the browser sign-in and consent while the CLI is waiting. The maintained
native client uses a loopback callback on port 8765 and saves its resource-bound
grant in the OS keyring. `status` inspects local credential metadata; `doctor`
checks the hosted connection and tool discovery.

## Grant read access

Open [AI connections](https://biologics.unibiointelligence.com/agent-studio) in
the same account. Inspect an existing connection before creating another one.
For an initial read check, use these settings:

| Setting | Value |
| --- | --- |
| Connection name | A name you recognize, such as Toolkit read access |
| OAuth client ID | `https://mcp.unibiointelligence.com/.well-known/ubi-cli-client.json` |
| MCP service | `https://mcp.unibiointelligence.com/mcp` |
| Projects | One existing Project you own |
| Permission | Read only |
| Allowed actions | Only `platform_whoami` and `list_projects` |
| Credit limit | Zero, enforced by read-only permission |
| Access duration | 1 hour |

Expand Allowed actions and remove the form's other default actions. Click Grant
access, then inspect the saved card and its Access details. The native CLI has
its own client ID; the Codex and ChatGPT client IDs describe different clients.

Verify the saved connection through the CLI:

```bash
ubi-biologics-cli platform_whoami
ubi-biologics-cli list_projects
```

Identity should report `verified_mcp_grant`, read permission, the exact client
and service above, your chosen Project and a zero-credit budget. Project listing
must stay within that scope. Scientific preview and submission require separate
execution consent; the read connection does not permit paid work.

## Resolve connection errors

| Error | Next step |
| --- | --- |
| `login_required` | Run `ubi-biologics-cli login` and complete the current browser flow. |
| `agent_grant_required` | Compare the saved connection's account, client ID, service and actions. A grant owned by another account cannot authorize this caller. |
| `agent_grant_expired` | Renew the existing connection in AI connections, preserving its scope and credit limit. |
| `contract_review_required` | Report the gateway/product contract mismatch to the operator; a different permission grant does not repair it. |

If the saved connection is correct but the CLI still uses an earlier account,
choose the intended account in its browser login and reconnect:

```bash
ubi-biologics-cli logout --forget-local
ubi-biologics-cli login
ubi-biologics-cli platform_whoami
```

`--forget-local` removes only this resource/client's local saved credentials;
it does not revoke the server-side OAuth grant. Ordinary `logout` requests
server revocation as well. If verification still fails, retain the safe error
code and correlation ID for support. Do not create duplicate connections.

## REST SDK credentials

Python and TypeScript SDK calls use the product REST API at
`https://biologics.unibiointelligence.com`. Supply a caller-owned REST access
token through your normal secret handling, for example `UBI_BIOLOGICS_TOKEN`.
The native CLI's MCP OAuth grant and a Supabase Dashboard operator token are
different credentials. Neither should be copied into the SDK token setting.

The SDK's credential must already authorize its target Project and operations.
Never embed an account token in a public browser bundle or include tokens in
support reports. The [hosted workflow guide](hosted-workflow.md) explains
preview, credit approval, submission and resuming existing Jobs.
