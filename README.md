# Ubi Biologics Toolkit

**By UniBio Intelligence**

Use the Ubi Biologics platform from a shell, Python or TypeScript. This
0.1.0 alpha candidate contains independently installable clients, selected
public API contracts and examples. Distribution is through the GitHub repository
and its source releases. npm and PyPI publication are disabled.

| Component | What you can do |
| --- | --- |
| [ubi-biologics-cli](packages/ubi-biologics-cli/README.md) | Log in, discover data/tools/modeling operations, inspect schemas and call the hosted MCP platform |
| [ubi-biologics-python](packages/ubi-biologics-python/README.md) | Use typed sync/async API calls and preview, submit, resume or cancel scientific workflows |
| [ubi-biologics-typescript](packages/ubi-biologics-typescript/README.md) | Integrate scientific workflows and generated API types |

## Install the component you need

From a GitHub checkout or extracted source release:

```bash
uv tool install --python 3.13 ./packages/ubi-biologics-cli
ubi-biologics-cli login
ubi-biologics-cli doctor
ubi-biologics-cli capabilities
ubi-biologics-cli tools
ubi-biologics-cli operations '{"capability":"modeling","search":"scenario"}'
```

Complete [CLI connection setup](docs/connect-cli.md) before product reads.
Browser login connects the CLI; a separate AI connection grants access to your
chosen Project. Start with read-only access, zero credits and a short expiry.

Python SDK installation: `python -m pip install ./packages/ubi-biologics-python`
(Python 3.13+). Build the TypeScript package using its component README;
the installed ESM library supports Node 22+ and compatible browser applications.
The clients do not install scientific solvers or a local platform server.
The Python SDK exposes `ubi_biologics_client` and `ubi_biologics_workflows`;
the CLI's internal module is `ubi_cli`. These import names are independent of
the component directory and installation names above.

The [scientific workflow tutorial](docs/hosted-workflow.md) previews inputs and
pricing before explicit submission. Use your own account and input resources.
Hosted operations retain platform permissions, quotas and credit charges.
The REST SDKs use a caller-owned `UBI_BIOLOGICS_TOKEN`, separate from the CLI's
resource-bound OAuth grant. See the [authentication guide](docs/connect-cli.md#rest-sdk-credentials).

See the [qualification record](docs/qualification.md) for the tested client
surface, retained live results and remaining publication gates.

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
