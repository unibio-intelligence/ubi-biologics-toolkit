import ast
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def refs(value):
    if isinstance(value, dict):
        if "$ref" in value:
            yield value["$ref"]
        for item in value.values():
            yield from refs(item)
    elif isinstance(value, list):
        for item in value:
            yield from refs(item)


def test_api_contains_only_selected_methods_and_resolvable_references():
    spec = json.loads((ROOT / "schemas/biologics-openapi.json").read_text())
    scope = json.loads((ROOT / "schemas/api-scope.json").read_text())
    assert set(spec["paths"]) == set(scope)
    methods = {"get", "put", "post", "delete", "patch", "head", "options", "trace"}
    for path, item in spec["paths"].items():
        assert set(item) & methods == set(scope[path])
    for ref in refs(spec):
        assert ref.startswith("#/components/")
        resolved = spec
        for part in ref[2:].split("/"):
            resolved = resolved[part.replace("~1", "/").replace("~0", "~")]


def test_cli_does_not_import_gateway_or_contain_local_backend():
    path = ROOT / "packages/ubi-biologics-cli/src/ubi_cli/cli.py"
    tree = ast.parse(path.read_text())
    imports = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    assert all(not (n.module or "").startswith(("ubi_server", "ubi_mcp_common")) for n in imports)
    assert all(n.module not in {"server", "gateway", "accounting", "auth"} for n in imports if n.level)
    assert not any(isinstance(n, ast.ClassDef) and n.name == "LocalGatewayClient" for n in ast.walk(tree))


def test_client_distribution_excludes_standalone_models_and_solvers():
    assert not (ROOT / "models").exists()
    assert not (ROOT / "runtimes").exists()
    assert not (ROOT / "packages/pkpd-reference").exists()
    assert not (ROOT / "Dockerfile.models").exists()
    for path in (ROOT / "packages").glob("*/pyproject.toml"):
        assert all(name not in path.read_text() for name in ("scipy", "numpy", "matplotlib", "ubi-mcp-common"))


def test_every_cli_module_has_only_standalone_imports():
    for path in (ROOT / "packages/ubi-biologics-cli/src/ubi_cli").rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith(("ubi_server", "ubi_mcp_common")), path
                if node.level == 1 and node.module:
                    module = node.module.split(".")[0]
                    assert (path.parent / f"{module}.py").exists(), (path, module)


def test_client_errors_do_not_echo_unreviewed_operation_or_message():
    from ubi_cli.errors import ServiceError

    result = ServiceError("login_required", "synthetic-private-message", operation="synthetic-private-operation").as_dict()
    assert "operation" not in result
    assert "synthetic-private" not in json.dumps(result)
