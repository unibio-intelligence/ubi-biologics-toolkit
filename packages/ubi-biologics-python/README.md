# Ubi Biologics Python client

Part of **Ubi Biologics Toolkit**, by **UniBio Intelligence**. Requires Python 3.13+.
From the release root, create a Python-only environment:

```bash
uv venv --python 3.13 .venv-client
uv pip install --python .venv-client/bin/python ./packages/ubi-biologics-python
```

Run your scripts with `.venv-client/bin/python` (on Windows, use
`.venv-client/Scripts/python.exe`). This installs the SDK without scientific
solvers or Node. Install this GitHub-distributed component locally; PyPI uploads
are disabled by package metadata. The distribution name is `ubi-biologics-python`;
its import modules are `ubi_biologics_client` and `ubi_biologics_workflows`.

```python
import os
from ubi_biologics_client import AuthenticatedClient
from ubi_biologics_client.api.platform import platform_whoami

client = AuthenticatedClient(
    base_url="https://biologics.unibiointelligence.com",
    token=os.environ["UBI_BIOLOGICS_TOKEN"],
    raise_on_unexpected_status=True,
)
with client:
    identity = platform_whoami.sync(client=client)
    print(identity)
```

`UBI_BIOLOGICS_TOKEN` must be a caller-owned product REST credential with access
to your resources. The CLI's MCP OAuth grant and Supabase Dashboard operator
credentials are separate. See the source release's
[authentication guide](../../docs/connect-cli.md#rest-sdk-credentials).

`ubi_biologics_client` contains generated sync/async endpoint modules.
`ubi_biologics_workflows` provides `ScientificRunsClient` and
`AsyncScientificRunsClient`: preview, price approval callback, signed-receipt
submission, stable retry keys, Job waiting, and protected Artifact downloads.
The [hosted workflow tutorial](../../docs/hosted-workflow.md) includes a runnable
preview-first example. Hosted execution requires an account and may cost credits.

The generated surface is the exact route/method allowlist in
`schemas/api-scope.json`, plus its referenced public schemas. It is an initial
scientific-workflow subset, not a complete SDK for every product feature.
No application backend is bundled. A timeout stops local waiting; use
`resume(job_id)` to continue or `cancel(job_id, reason=...)` to request server-side
cancellation. Submission retries preserve one idempotency key.

After the full contributor setup, regenerate through `uv run python scripts/generate-clients.py` at the release root.
Do not edit generated modules by hand. Apache-2.0; third-party dependencies
retain their licenses.
