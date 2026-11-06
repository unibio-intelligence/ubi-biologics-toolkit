# Support and compatibility

Ubi Biologics Toolkit 0.1.0 alpha is maintained by UniBio Intelligence.
Python clients require Python 3.13+; TypeScript development requires Node 22+.
The TypeScript distribution is ESM. During alpha, schemas may change between
releases: pin your installed package version and inspect release notes.

The SDK covers the explicit route/method allowlist in schemas/api-scope.json.
The CLI uses the platform's canonical data, tools and modeling contract.
Use the server catalog and schema to discover currently authorized operations.
Installed clients do not grant account access or scientific compute.
For `login_required`, `agent_grant_required` or expired Project consent, use the
[connection guide](connect-cli.md). Include only safe error codes and correlation
IDs when reporting an authorization problem.

Report issues at https://github.com/unibio-intelligence/ubi-biologics-toolkit/issues
with component version, environment, expected result and a small public reproduction.
Do not include tokens or private research data. Use SECURITY.md for vulnerabilities.
There is no LTS or guaranteed response-time commitment for this initial alpha.
Standalone model and engine questions belong to QSPQuest.
