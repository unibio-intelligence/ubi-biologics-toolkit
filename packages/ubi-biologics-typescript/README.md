# Ubi Biologics TypeScript client

Part of **Ubi Biologics Toolkit**, by **UniBio Intelligence**. This ESM library supports
Node 22+ and compatible browser applications. Python and scientific solvers
are not required.

Build a local installable tarball from the release root:

```bash
npm --prefix packages/ubi-biologics-typescript ci --ignore-scripts
mkdir -p dist
(cd packages/ubi-biologics-typescript && npm pack --pack-destination ../../dist)
```

Install the resulting `ubi-biologics-typescript-0.1.0-alpha.1.tgz` into
your application with `npm install /path/to/the/tarball.tgz`. The package name
is `ubi-biologics-typescript`. It is distributed through GitHub and has
`private: true` to disable npm publication while allowing local installation.

```typescript
import { ScientificRunsClient } from 'ubi-biologics-typescript';

const client = new ScientificRunsClient({
  baseUrl: 'https://biologics.unibiointelligence.com',
  accessToken: () => process.env.UBI_BIOLOGICS_TOKEN ?? null
});
// draft follows the RunCreateRequest contract and uses your own input resources.
// Preview before deciding whether to submit a chargeable scientific Job:
// const preview = await client.preview(draft);
```

Use a caller-owned product REST credential for `UBI_BIOLOGICS_TOKEN`. The CLI's
MCP OAuth grant and Supabase Dashboard operator credentials are separate. See
the source release's [authentication guide](../../docs/connect-cli.md#rest-sdk-credentials).

Exports include the scientific workflow client, errors, and generated OpenAPI
`paths`, `components`, and `operations` types. The generated endpoint types
cover the route/method allowlist in `schemas/api-scope.json`; the executable
client covers scientific Run/Job/Artifact workflows. It is not a generated
method-per-endpoint REST implementation.

Workflow calls preserve preview receipts, price approval, submission retry
identity, Job events/polling, and protected Artifact retrieval. See the release's
hosted workflow tutorial for authentication and execution boundaries.
Apache-2.0; dependencies retain their own licenses.
