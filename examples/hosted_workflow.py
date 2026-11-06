"""Preview a caller-owned scientific draft; execute only with an explicit credit cap."""
import argparse
import json
import math
import os
from pathlib import Path

from ubi_biologics_client import AuthenticatedClient
from ubi_biologics_workflows import ScientificRunsClient


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="Run draft JSON containing your own inputs")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--max-credits", type=float)
    args = parser.parse_args()
    if args.execute and (args.max_credits is None or not math.isfinite(args.max_credits) or args.max_credits < 0):
        parser.error("--execute requires a finite, nonnegative --max-credits")
    token = os.getenv("UBI_BIOLOGICS_TOKEN")
    if not token:
        parser.error("Set UBI_BIOLOGICS_TOKEN to your account's bearer token")
    draft = json.loads(args.draft.read_text())
    client = AuthenticatedClient(
        base_url="https://biologics.unibiointelligence.com",
        token=token, raise_on_unexpected_status=True,
    )
    with client:
        workflow = ScientificRunsClient(client)
        if not args.execute:
            preview = workflow.preview(draft)
            # Preview receipts are credentials for submission; print only useful review fields.
            print(json.dumps({"pricing": preview.get("pricing"), "valid": preview.get("valid"), "approval_required": preview.get("approval_required")}, indent=2))
            return
        result = workflow.run(
            draft,
            approve=lambda preview: preview["pricing"]["credit_cost"] <= args.max_credits,
            on_submitted=lambda submission: print(json.dumps({"job_ids": [job["id"] for job in submission["jobs"]]})),
        )
        print(json.dumps({"jobs": [job["id"] for job in result.jobs], "artifact_count": len(result.artifacts)}))


if __name__ == "__main__":
    main()
