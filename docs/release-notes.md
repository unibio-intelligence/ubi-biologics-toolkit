# Release notes

## 0.1.0 alpha candidate

- Standardize component directories and installation names as
  `ubi-biologics-cli`, `ubi-biologics-python` and `ubi-biologics-typescript`.
  The shell command is `ubi-biologics-cli`; Python import modules and the hosted
  native OAuth client identity are preserved.
- Use GitHub-only distribution, with npm and PyPI upload guards and documented
  local installation. Registry publisher setup is outside this release.
- Refresh provenance against committed platform/product main revisions and a
  newly fetched hosted OpenAPI document; the selected 25-path, 29-operation
  contract and client runtime sources are unchanged.
- Document the separate native OAuth login and project-scoped AI connection,
  same-account reconnect, one-hour read consent and zero-credit setup.
- Distinguish REST SDK credentials from MCP and Dashboard operator credentials,
  and retain the completed CLI/SDK qualification boundaries.
- Refresh the selected contract from the current hosted public API schema.
- Discover named MCP tools from the caller-authorized remote catalog and reject
  retired generic execution commands.
- Use FastMCP 4.1.2, bundle the native callback's Ubi branding, and sanitize
  dependency diagnostics without installing private platform modules.
- Rename the public client distribution to Ubi Biologics Toolkit.
- Use the canonical platform CLI tool contract, native OAuth client and secure
  resource-bound credential handling; remove the retired gateway aliases.
- Refresh the selected Python/TypeScript API contract and generated clients.
- Keep preview receipts, explicit price approval, stable submission retry keys,
  resumable Job waiting, cancellation and protected Artifact retrieval.
- Remove duplicate model bundles, solver packages, Julia runtimes and numerical
  fixtures. QSPQuest is the maintained standalone engine and model-library route.

This is an unpublished candidate. No public source, registry package or image
has been published by its preparation. Hosted access retains platform permissions
and charges; package installation does not provision an account.
