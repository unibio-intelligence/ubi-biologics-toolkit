# Release preparation

**Publication is on hold.** The public ubi-biologics-toolkit repository is empty.
Do not push source, branches or tags, or publish packages/images without a new
explicit owner instruction. CI verifies only; it has no publishing jobs or credentials.

The canonical source is private ubi-tools/distribution/ubi-biologics-toolkit/.
Implement community fixes privately and export only this reviewed subtree with
fresh public history. The old combined Methods candidate and model evidence are
historical private records. QSPQuest owns the maintained standalone models.

Before selecting a release:

1. Refresh reviewed client inputs with the private preparation helper, regenerate
   from the bundled API schema and confirm generation produces no differences.
2. Run Python and TypeScript suites, including actual MCP transport, native OAuth
   lifecycle and safe error handling. Run authenticated preproduction qualification
   against the exact intended hosted endpoints. Record what is and is not exercised;
   deterministic fixtures do not establish a live login or production workflow.
   Verify that /.well-known/ubi-cli-client.json is served with the reviewed native
   identity and exact loopback callback, or configure an explicitly approved static
   client. Do not publish a default-login quickstart against a missing document.
   Compare the deployed `tools/list` with the named-tool contract used by the
   candidate. A successful login against an older generic gateway does not
   qualify named scientific reads or executions. Complete the separate
   [project-scoped AI connection](connect-cli.md), verify identity and Project
   reads, and retain the resolved client/resource/permission/expiry/budget bounds.
   Keep a deployment mismatch as
   an explicit gate; do not add compatibility aliases to make the check pass.
3. Build both Python wheels/source distributions and the local TypeScript tarball.
   Install outside the source checkout; verify imports, CLI help and workflow exports.
4. Create the deterministic source archive with scripts/package-release.py, verify
   its hashes and build Dockerfile.verify from the clean extracted archive.
5. Review exact package/source contents, licenses, dependency inventory, final
   repository/issue links and GitHub repository permissions.
6. Submit the final unchanged candidate to the required Fable review and retain
   its outcome privately. Substantive changes require re-review before publication.

```bash
uv build --package ubi-biologics-cli
uv build --package ubi-biologics-python
(cd packages/ubi-biologics-typescript && npm pack --pack-destination ../../dist)
uv run python scripts/package-release.py --output dist/ubi-biologics-toolkit-0.1.0-alpha.1.tar.gz
docker build -f Dockerfile.verify -t ubi-biologics-toolkit:verify .
```

When separately authorized, export the exact reviewed archive to
unibio-intelligence/ubi-biologics-toolkit with fresh public history. GitHub is
the only distribution destination. Record released versions and immutable
checksums; users install from the checkout or locally built package files.

Do not publish to npm or PyPI. Registry sign-in, package-name reservation,
publisher verification and registry tokens are outside the current release.
The TypeScript package has `private: true`; both Python distributions carry
`Private :: Do Not Upload`. These guards preserve local packing and installation.
Removing them requires a new owner decision and review.
