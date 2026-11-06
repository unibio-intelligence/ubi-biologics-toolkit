# Ubi Biologics Toolkit

**By UniBio Intelligence**

Use the Ubi Biologics platform from a shell, Python or TypeScript. This
0.1.0 alpha release contains independently installable clients, selected
public API contracts and examples. Distribution is through the GitHub repository
and its source releases. npm and PyPI publication are disabled.

| Component | What you can do |
| --- | --- |
| [ubi-biologics-cli](#cli-install-log-in-and-read-your-projects) | Log in, discover data/tools/modeling operations, inspect schemas and call the hosted MCP platform |
| [ubi-biologics-python](#python-install-and-read-one-project) | Use typed sync/async API calls and preview, submit, resume or cancel scientific workflows |
| [ubi-biologics-typescript](#typescript-install-and-read-one-project) | Integrate scientific workflows and generated API types |

## Getting started

Install only the component you need. The first examples below read an existing
Project; they do not create a Project, submit a scientific Job or approve spending.
Sign in to [Ubi Biologics](https://biologics.unibiointelligence.com), open a Project
you are authorized to use and copy its ID from the Project page URL.

| Component | Requirements | Authentication |
| --- | --- | --- |
| CLI | Git, [uv](https://docs.astral.sh/uv/getting-started/installation/), Python 3.13+ | Browser login **and** a Project-scoped AI connection |
| Python | Git, uv, Python 3.13+ | A product REST credential authorized for the Project |
| TypeScript | Node 22+ and npm | A product REST credential authorized for the Project |

The CLI/Python commands use the versioned source checkout below. TypeScript can
install its built tarball directly from the [GitHub release](https://github.com/unibio-intelligence/ubi-biologics-toolkit/releases/tag/v0.1.0-alpha.1).
The shell commands use macOS/Linux paths; Windows Python environments use
`Scripts/python.exe` in place of `bin/python`.

```bash
git clone --branch v0.1.0-alpha.1 --depth 1 \
  https://github.com/unibio-intelligence/ubi-biologics-toolkit.git
cd ubi-biologics-toolkit
```

### CLI: install, log in and read your Projects

From the checkout root:

```bash
uv tool install --python 3.13 ./packages/ubi-biologics-cli
ubi-biologics-cli --version
ubi-biologics-cli login
ubi-biologics-cli doctor
```

Complete the browser sign-in while the CLI is waiting. Credentials are saved
in the OS keyring. If your shell cannot find `ubi-biologics-cli`, run
`uv tool update-shell` and open a new terminal. `doctor` checks the connection;
Project access requires the next step as well.

In the **same Ubi account**, open [AI connections](https://biologics.unibiointelligence.com/agent-studio).
Use or create a connection with these initial read-only settings:

| Setting | Value |
| --- | --- |
| Connection name | Toolkit read access |
| OAuth client ID | `https://mcp.unibiointelligence.com/.well-known/ubi-cli-client.json` |
| MCP service | `https://mcp.unibiointelligence.com/mcp` |
| Projects | One existing Project you own |
| Permission | Read only |
| Allowed actions | Only `platform_whoami` and `list_projects`; remove other default actions |
| Credit limit | Zero |
| Duration | 1 hour |

Click **Grant access**, inspect the saved connection, then run your first reads:

```bash
ubi-biologics-cli platform_whoami
ubi-biologics-cli list_projects
```

Expect JSON describing the verified grant and only the authorized Project.
Discover available tools with `ubi-biologics-cli tools`. See the
[connection guide](docs/connect-cli.md) for account alignment, renewal and logout.
The two-action read grant does not authorize scientific previews or submissions.

### SDK credentials and Project access

Python and TypeScript use the product REST API. Their clients do not implement
the CLI's interactive browser login, and the CLI AI connection above does not
issue an SDK credential.

Use an existing, caller-owned REST credential or ask your Organization owner or
administrator to issue one in **Agent Studio → Identity & credentials**. For the
first examples, restrict it to your chosen Project and `projects:read`, remove
unneeded default scopes and use a short expiry. Keep the issued secret in your
normal secret manager and provide it to your process as `UBI_BIOLOGICS_TOKEN`.
Set `UBI_PROJECT_ID` to that Project's ID:

```bash
export UBI_PROJECT_ID="replace-with-your-authorized-project-id"
```

The token must be authorized for this Project. A native MCP OAuth token or a
Supabase Dashboard operator token is not a product REST credential. Do not put
the REST credential in source files, commit it or embed it in a public browser
bundle. See [REST authentication](docs/connect-cli.md#rest-sdk-credentials).

### Python: install and read one Project

From the checkout root, create a separate environment and install the SDK:

```bash
uv venv --python 3.13 .venv-client
uv pip install --python .venv-client/bin/python ./packages/ubi-biologics-python
```

Complete [SDK credential setup](#sdk-credentials-and-project-access), then save
this as `first_project.py`:

```python
import os

from ubi_biologics_client import AuthenticatedClient
from ubi_biologics_client.api.platform import get_project
from ubi_biologics_client.models.api_envelope_project_response import APIEnvelopeProjectResponse

token = os.environ.get("UBI_BIOLOGICS_TOKEN")
project_id = os.environ.get("UBI_PROJECT_ID")
if not token or not project_id:
    raise SystemExit("Set UBI_BIOLOGICS_TOKEN and UBI_PROJECT_ID first.")

with AuthenticatedClient(
    base_url="https://biologics.unibiointelligence.com",
    token=token,
    raise_on_unexpected_status=True,
) as client:
    response = get_project.sync_detailed(project_id=project_id, client=client)
    if response.status_code != 200 or not isinstance(response.parsed, APIEnvelopeProjectResponse):
        raise SystemExit(f"Project read failed (HTTP {response.status_code}); check your credential and Project access.")
    project = response.parsed.data
    print(f"{project.id}: {project.name}")
```

Run it with the environment's Python:

```bash
.venv-client/bin/python first_project.py
```

Expect your Project's ID and name. The distribution is named `ubi-biologics-python`;
its imports are `ubi_biologics_client` (generated sync/async REST calls) and
`ubi_biologics_workflows` (scientific workflows). See the [Python guide](packages/ubi-biologics-python/README.md).

### TypeScript: install and read one Project

Create a small Node application, or use your existing one. npm installs the
SDK tarball **from GitHub**; no npm registry release is required. The development
dependencies below compile the TypeScript example.

```bash
mkdir ubi-typescript-quickstart
cd ubi-typescript-quickstart
npm init -y
npm install "https://github.com/unibio-intelligence/ubi-biologics-toolkit/releases/download/v0.1.0-alpha.1/ubi-biologics-typescript-0.1.0-alpha.1.tgz"
npm install --save-dev typescript@5.9.3 @types/node@22.18.6
```

Complete [SDK credential setup](#sdk-credentials-and-project-access) in this
terminal, then save the following as `first-project.mts`. This Project read uses the SDK's generated response type
with Node's `fetch`. The package also exports `ScientificRunsClient` for
Run/Job/Artifact workflows; it does not generate a callable method for every REST endpoint.

```typescript
import type { components } from 'ubi-biologics-typescript';

type ProjectEnvelope = components['schemas']['APIEnvelope_ProjectResponse_'];

const token = process.env.UBI_BIOLOGICS_TOKEN;
const projectId = process.env.UBI_PROJECT_ID;
if (!token || !projectId) {
  throw new Error('Set UBI_BIOLOGICS_TOKEN and UBI_PROJECT_ID first.');
}

const response = await fetch(
  `https://biologics.unibiointelligence.com/api/v1/projects/${encodeURIComponent(projectId)}`,
  { headers: { Authorization: `Bearer ${token}` } }
);
if (!response.ok) {
  throw new Error(`Project read failed (HTTP ${response.status}); check your credential and Project access.`);
}
const { data: project } = (await response.json()) as ProjectEnvelope;
console.log(`${project.id}: ${project.name}`);
```

Compile and run it:

```bash
npx tsc first-project.mts --module NodeNext --target ES2022 --outDir dist
node dist/first-project.mjs
```

Expect the same authorized Project's ID and name. See the
[TypeScript guide](packages/ubi-biologics-typescript/README.md) for workflow exports
and building a tarball from source.

### Next steps and common errors

| Symptom | What to check |
| --- | --- |
| CLI `login_required` | Run `ubi-biologics-cli login` and finish the browser flow. |
| CLI `agent_grant_required` or `agent_grant_expired` | Check the saved AI connection's account, exact client ID, Project, actions and expiry. |
| SDK HTTP 401 | Check that the product REST credential is present and unexpired. |
| SDK HTTP 403 or 404 | Check the Project ID, credential scope and Project access with your administrator. |

The [scientific workflow tutorial](docs/hosted-workflow.md) explains previews,
pricing, explicit execution approval, stable retry keys and resuming Jobs.
Scientific workflows need additional authorization and may spend credits;
read-only onboarding does not grant execution access. The clients do not install
scientific solvers or a local platform server. See the
[qualification record](docs/qualification.md) for the tested client surface and
retained live-result boundaries.

## Standalone models

The maintained standalone simulation engine and model library belong to
**QSPQuest**. This toolkit does not ship model definitions, scientific fixtures,
Julia runtimes or duplicate solver implementations. Use the QSPQuest engine and
companion model-library documentation for local simulation. A hosted modeling
capability and a standalone model may have different evidence and release status.

## Develop and verify

Contributor tools: Python 3.13+, uv and Node 22+.

```bash
uv sync --frozen --all-packages --group dev
npm ci --ignore-scripts
npm --prefix packages/ubi-biologics-typescript ci --ignore-scripts
uv run python scripts/generate-clients.py
uv run pytest
npm --prefix packages/ubi-biologics-typescript test
npm --prefix packages/ubi-biologics-typescript run build
uv build --package ubi-biologics-cli
uv build --package ubi-biologics-python
```

SDK generation reads the bundled selected OpenAPI contract. Public source is
exported from a reviewed private distribution; platform server, auth proxy,
accounting, workers, private data and Git history are excluded.
See [CONTRIBUTING.md](CONTRIBUTING.md), [support](docs/support.md),
[release notes](docs/release-notes.md) and [release preparation](docs/releasing.md).
Apache-2.0 covers UniBio Intelligence-owned client code; dependencies retain
their licenses. See [NOTICE](NOTICE).
