"""Create a deterministic source archive from the explicit publication allowlist."""
from __future__ import annotations

import argparse
import gzip
from hashlib import sha256
import io
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "README.md", "LICENSE", "NOTICE", "CITATION.cff", "CONTRIBUTING.md", "SECURITY.md",
    "SOURCE_MANIFEST.json", "pyproject.toml", "uv.lock", "package.json", "package-lock.json",
    "python-client-config.yaml", ".gitignore", ".dockerignore", "Dockerfile.verify",
    ".github/workflows/ci.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
}
DIRS = {"docs", "schemas", "examples", "scripts", "tests"}
PACKAGES = {"ubi-biologics-cli", "ubi-biologics-python", "ubi-biologics-typescript"}
PACKAGE_FILES = {"pyproject.toml", "package.json", "package-lock.json", "tsconfig.json", "README.md", "LICENSE", "LICENSE.upstream", "THIRD_PARTY_NOTICES.md"}
SKIP = {"__pycache__", ".pytest_cache", ".ruff_cache", "node_modules", ".venv", "dist", "build"}


def selected_files():
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if any(part in SKIP or part.startswith(".venv-") or part.endswith(".egg-info") for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Symlinks are not publication inputs: {relative}")
        if not path.is_file() or path.suffix in {".pyc", ".pyo"}:
            continue
        parts = relative.parts
        allowed = relative.as_posix() in FILES or parts[0] in DIRS
        if len(parts) >= 3 and parts[0] == "packages" and parts[1] in PACKAGES:
            allowed = (len(parts) == 3 and parts[2] in PACKAGE_FILES) or parts[2] in {"src", "tests"}
        if allowed:
            if path.name.startswith(".env") or path.suffix in {".pem", ".key", ".parquet", ".pdf", ".docx", ".sqlite", ".pt", ".pkl"}:
                raise ValueError(f"Unexpected publication input: {relative}")
            yield relative, path.read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inputs = list(selected_files())
    manifest = {str(path): sha256(data).hexdigest() for path, data in inputs}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as compressed, tarfile.open(fileobj=compressed, mode="w") as archive:
        for path, data in [*inputs, (Path("RELEASE_MANIFEST.json"), (json.dumps(manifest, indent=2, sort_keys=True)+"\n").encode())]:
            entry = tarfile.TarInfo(f"ubi-biologics-toolkit/{path}")
            entry.size, entry.mode, entry.mtime = len(data), 0o644, 0
            archive.addfile(entry, io.BytesIO(data))
    digest = sha256(args.output.read_bytes()).hexdigest()
    args.output.with_suffix(args.output.suffix + ".sha256").write_text(f"{digest}  {args.output.name}\n")
    print(json.dumps({"archive": str(args.output), "files": len(inputs)+1, "sha256": digest}))


if __name__ == "__main__":
    main()
