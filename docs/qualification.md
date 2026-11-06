# Client qualification

This unpublished alpha has retained live qualification for the CLI, Python SDK
and TypeScript SDK. The November 5, 2026 refresh updates provenance from committed
sources and documents the required Project consent flow. Component names now use
`ubi-biologics-*`; the CLI command, version lookup and login hints follow that name.
The selected API contract, OAuth identity and scientific workflow behavior are
unchanged. Local checks cover the renamed packages; the live results below were
recorded before that naming change.

## Verified live behavior

- Installed native CLI: all eight read checks passed, covering connection/tool
  discovery, capabilities, identity, Project listing, resources, prompts and quota.
- Resolved CLI grant: exact native client and main MCP resource, read permission,
  only identity and Project listing, one Project, zero credits and a one-hour
  lifetime. Project listing returned only the approved Project.
- Installed Python and TypeScript SDKs: one approved scientific workflow each
  reached success, with Job events, protected Artifact downloads, matching
  checksums and original-key replay returning the same Job.

Live results are evidence for those runs and accounts. Their temporary grants
expire; the [connection guide](connect-cli.md) describes setting up your own
access. The documentation/provenance refresh does not submit additional paid
Jobs or treat saved settings alone as proof of authorization.

## Refreshed source boundary

| Input | Revision or SHA-256 |
| --- | --- |
| Platform main | `66a4c0e227eb7650f5ee612c4b3140cd48270a5c` |
| Product main | `809c550a7bb597a704d0457573a7d78e2d95bbfd` |
| Hosted public OpenAPI | `330a625aa3e3456b9540744ba224ead6d75c85f9b2673156a3b6d1d5dcc5862a` |

`SOURCE_MANIFEST.json` records every selected input hash. The SDK selection is
25 paths and 29 operations with their transitive schemas. Generated clients,
standalone exports, package tests and deterministic source packaging are checked
locally. Private platform servers, workers, accounting, research data, credentials
and model/solver bundles remain outside the client distribution.

## Publication status

Publication is held by the owner. Exact-candidate Fable review, GitHub permission
verification and explicit publication authorization remain separate gates.
Distribution is GitHub-only; npm and PyPI publisher checks are not release gates.
The TypeScript package disables npm publication and both Python distributions
disable PyPI uploads while remaining locally installable. Client qualification
does not establish the status of a later application/gateway deployment or its
recovery configuration. CI verifies only and does not deploy or publish.
