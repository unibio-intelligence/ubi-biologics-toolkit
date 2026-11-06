# Preview and run a scientific workflow

This tutorial requires Python 3.13+ and uv. The commands below install only
the Python SDK into a uv-managed environment. Node and scientific solvers are
not required. Supply a caller-owned bearer token through
`UBI_BIOLOGICS_TOKEN` using your normal secret handling.
This is a product REST credential, separate from the CLI's MCP OAuth grant and
Supabase Dashboard operator access. See [authentication and Project access](connect-cli.md).

Choose a released capability through the product catalog or SDK's capability
endpoints. Inspect its current input roles and parameter schema. Prepare an
immutable input Dataset/Asset in your own Project through the product UI or
its supported ingestion API. This initial SDK does not bundle every ingestion
workflow. Resource IDs must belong to your account.

Create `draft.json` using the capability's exact contract:

```json
{
  "capability_id": "<released capability id>",
  "inputs": [
    {
      "role": "<role declared by the capability>",
      "resource_kind": "dataset_version",
      "resource_id": "<your immutable Dataset Version id>"
    }
  ],
  "parameters": {}
}
```

The placeholders must be replaced. Optional `destination_project_id` selects
an existing Project; otherwise the workflow resolves your default Project.

```bash
uv run --no-project --python 3.13 --with ./packages/ubi-biologics-python python examples/hosted_workflow.py draft.json
```

This previews the request and prints pricing without submitting a compute Job.
Default Project resolution may create your default Project if none exists.
To authorize execution within a credit ceiling:

```bash
uv run --no-project --python 3.13 --with ./packages/ubi-biologics-python python examples/hosted_workflow.py draft.json --execute --max-credits 2
```

The client obtains a fresh preview, applies the ceiling, submits its receipt,
and preserves one idempotency key across submission retries. The server makes
the final authorization, readiness, and pricing decision. A required approval
must be handled through the product's approval workflow.

The callback prints Job IDs immediately after submission. A local wait timeout
does not cancel the Job: use `ScientificRunsClient.resume(job_id)` afterward.
Use `cancel(job_id, reason="...")` for an explicit cancellation request.

For TypeScript, use `ScientificRunsClient` from the locally built
`ubi-biologics-typescript` tarball (see its component README) with your token
provider, then `preview(draft)` or `run(draft, { approve: preview => ... })`.
Never embed an account token in a public browser bundle.

Offline tests use mocked transport and exercise receipts, retry identity,
publication, and downloads. They do not certify a live production run. The
release preparation does not spend credits or submit customer workloads.
