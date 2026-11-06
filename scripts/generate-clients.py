"""Regenerate the public SDK contracts without importing the private platform."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    subprocess.run([
        sys.executable, "-m", "openapi_python_client", "generate",
        "--path", str(ROOT / "schemas/biologics-openapi.json"),
        "--config", str(ROOT / "python-client-config.yaml"),
        "--meta", "none", "--output-path",
        str(ROOT / "packages/ubi-biologics-python/src/ubi_biologics_client"),
        "--overwrite", "--fail-on-warning",
    ], check=True, cwd=ROOT)
    subprocess.run([
        str(ROOT / "node_modules/.bin/openapi-typescript"),
        str(ROOT / "schemas/biologics-openapi.json"), "--output",
        str(ROOT / "packages/ubi-biologics-typescript/src/schema.d.ts"),
    ], check=True, cwd=ROOT)

if __name__ == "__main__":
    main()
