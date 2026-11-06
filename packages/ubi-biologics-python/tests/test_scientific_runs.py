from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import httpx
import pytest

from ubi_biologics_client import AuthenticatedClient  # noqa: E402
from ubi_biologics_workflows import (  # noqa: E402
    ApprovalRequiredError,
    AsyncScientificRunsClient,
    PublicationError,
    ScientificRunsClient,
)


def _envelope(data):
    return {"data": data, "meta": {"request_id": "req_test", "trace_id": "trace_test"}}


def _job(state: str = "succeeded", publication_state: str = "published"):
    return {
        "id": "job_1",
        "run_id": "run_1",
        "destination_project_id": "project_1",
        "state": state,
        "resource_class": "cpu-small",
        "attempt_count": 1,
        "max_attempts": 3,
        "cancellation_requested": False,
        "publication_state": publication_state,
        "staged_outputs": [],
        "pricing": {"credit_cost": 2, "pricing_note": "fixed"},
        "created_at": "2026-08-19T00:00:00Z",
        "updated_at": "2026-08-19T00:00:01Z",
        "completed_at": "2026-08-19T00:00:01Z",
    }


def _preview(approval_required: bool = False):
    return {
        "preview_digest": "preview_digest_1",
        "preview_receipt": "signed-preview-receipt",
        "approval_required": approval_required,
        "pricing": {"credit_cost": 2, "pricing_note": "fixed"},
    }


def _submission():
    return {"jobs": [_job("queued", "pending")], "run": {"id": "run_1"}}


def _artifact():
    return {"id": "artifact_1", "name": "result.json", "media_type": "application/json"}


def test_sync_workflow_reuses_project_and_submission_key_then_downloads_artifact():
    calls: list[tuple[str, str]] = []
    submit_keys: list[str] = []
    submit_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal submit_count
        calls.append((request.method, request.url.path))
        if request.url.path == "/api/v1/projects/default":
            return httpx.Response(200, json=_envelope({"id": "project_1"}))
        if request.url.path == "/api/v1/runs/preview":
            assert json.loads(request.content)["destination_project_id"] == "project_1"
            return httpx.Response(200, json=_envelope(_preview()))
        if request.url.path == "/api/v1/runs" and request.method == "POST":
            submit_count += 1
            submit_keys.append(request.headers["Idempotency-Key"])
            assert (
                json.loads(request.content)["preview_receipt"]
                == "signed-preview-receipt"
            )
            if submit_count == 1:
                return httpx.Response(
                    503,
                    json={
                        "error": {
                            "code": "CAPACITY_UNAVAILABLE",
                            "message": "retry",
                            "retryable": True,
                        }
                    },
                )
            return httpx.Response(202, json=_envelope(_submission()))
        if request.url.path.endswith("/events/stream"):
            event = {
                "id": "event_1",
                "job_id": "job_1",
                "sequence": 1,
                "event_type": "job.started",
                "data": {},
                "created_at": "2026-08-19T00:00:00Z",
            }
            return httpx.Response(
                200,
                text=f"id: 1\nevent: job.started\ndata: {json.dumps(event)}\n\n",
                headers={"content-type": "text/event-stream"},
            )
        if request.url.path == "/api/v1/jobs/job_1":
            return httpx.Response(200, json=_envelope(_job()))
        if request.url.path == "/api/v1/jobs/job_1/detail":
            return httpx.Response(200, json=_envelope({"artifacts": [_artifact()]}))
        if request.url.path == "/api/v1/artifacts/artifact_1/content":
            return httpx.Response(200, content=b'{"ok":true}')
        raise AssertionError(f"Unexpected request: {request.method} {request.url}")

    raw_client = httpx.Client(
        base_url="https://biologics.unibiointelligence.com",
        transport=httpx.MockTransport(handler),
    )
    generated = AuthenticatedClient(
        base_url="https://biologics.unibiointelligence.com", token="token"
    ).set_httpx_client(raw_client)
    events = []
    state_changes = []
    submitted_at: list[int] = []
    workflow = ScientificRunsClient(generated, sleep=lambda _seconds: None)

    result = workflow.run(
        {"capability_id": "abnumber.annotate"},
        idempotency_key="stable-key",
        on_submitted=lambda _submission: submitted_at.append(len(calls)),
        on_event=events.append,
        on_state_change=state_changes.append,
        download_artifacts=True,
    )

    assert submit_keys == ["stable-key", "stable-key"]
    assert submitted_at[0] < next(
        index
        for index, call in enumerate(calls, start=1)
        if call[1] == "/api/v1/jobs/job_1"
    )
    assert Counter(path for _, path in calls)["/api/v1/projects/default"] == 1
    assert events[0]["sequence"] == 1
    assert [job["state"] for job in state_changes] == ["succeeded"]
    assert result.jobs[0]["state"] == "succeeded"
    assert result.artifacts[0]["id"] == "artifact_1"
    assert result.artifact_contents["artifact_1"] == b'{"ok":true}'


def test_sync_cancel_uses_explicit_governed_endpoint_and_stable_key():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/jobs/job_1/cancel"
        assert request.headers["Idempotency-Key"] == "cancel-key"
        assert json.loads(request.content) == {"reason": "user request"}
        return httpx.Response(200, json=_envelope(_job("cancel_requested", "pending")))

    generated = AuthenticatedClient(base_url="https://example.test", token="token")
    generated.set_httpx_client(
        httpx.Client(
            base_url="https://example.test", transport=httpx.MockTransport(handler)
        )
    )

    cancelled = ScientificRunsClient(generated).cancel(
        "job_1", reason="user request", idempotency_key="cancel-key"
    )

    assert cancelled["state"] == "cancel_requested"


def test_sync_exact_artifact_download_enforces_ceiling_size_and_checksum():
    content = b'{"ok":true}'

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/artifacts/artifact_1/content"
        return httpx.Response(
            200,
            headers={"content-length": str(len(content))},
            content=content,
        )

    generated = AuthenticatedClient(base_url="https://example.test", token="token")
    generated.set_httpx_client(
        httpx.Client(
            base_url="https://example.test", transport=httpx.MockTransport(handler)
        )
    )
    workflow = ScientificRunsClient(generated)
    artifact = {
        "id": "artifact_1",
        "size_bytes": len(content),
        "checksum_hex": hashlib.sha256(content).hexdigest(),
    }

    assert workflow.download_artifact_exact(artifact, max_bytes=1024) == content
    with pytest.raises(PublicationError) as too_large:
        workflow.download_artifact_exact(artifact, max_bytes=4)
    assert too_large.value.code == "ARTIFACT_TOO_LARGE"

    corrupt_metadata = {**artifact, "checksum_hex": "0" * 64}
    with pytest.raises(PublicationError) as corrupt:
        workflow.download_artifact_exact(corrupt_metadata, max_bytes=1024)
    assert corrupt.value.code == "ARTIFACT_INTEGRITY_MISMATCH"


def test_sync_workflow_falls_back_to_polling_and_detects_publication_failure():
    states = iter([_job("running", "pending"), _job("succeeded", "failed")])
    sleeps: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/events/stream"):
            return httpx.Response(200, json={"not": "sse"})
        if request.url.path == "/api/v1/jobs/job_1":
            return httpx.Response(
                200, json=_envelope(next(states)), headers={"Retry-After": "0.01"}
            )
        raise AssertionError(str(request.url))

    generated = AuthenticatedClient(base_url="https://example.test", token="token")
    generated.set_httpx_client(
        httpx.Client(
            base_url="https://example.test", transport=httpx.MockTransport(handler)
        )
    )
    workflow = ScientificRunsClient(generated, sleep=sleeps.append)

    with pytest.raises(PublicationError) as caught:
        workflow.wait_for_job("job_1")
    assert caught.value.code == "JOB_PUBLICATION_INCOMPLETE"
    assert sleeps == [0.01]


def test_sync_workflow_reads_retryable_stream_error_before_polling_fallback():
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        if request.url.path.endswith("/events/stream"):
            return httpx.Response(
                503,
                json={
                    "error": {
                        "code": "CAPACITY_UNAVAILABLE",
                        "message": "stream temporarily unavailable",
                        "retryable": True,
                    }
                },
            )
        if request.url.path == "/api/v1/jobs/job_1":
            return httpx.Response(200, json=_envelope(_job()))
        raise AssertionError(str(request.url))

    generated = AuthenticatedClient(base_url="https://example.test", token="token")
    generated.set_httpx_client(
        httpx.Client(
            base_url="https://example.test", transport=httpx.MockTransport(handler)
        )
    )

    job = ScientificRunsClient(generated).wait_for_job("job_1")

    assert job["state"] == "succeeded"
    assert calls == [
        "/api/v1/jobs/job_1/events/stream",
        "/api/v1/jobs/job_1",
    ]


def test_sync_workflow_stops_before_submission_when_platform_approval_is_required():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/v1/runs/preview":
            return httpx.Response(200, json=_envelope(_preview(True)))
        raise AssertionError("Approval-required workflow must not submit directly")

    generated = AuthenticatedClient(base_url="https://example.test", token="token")
    generated.set_httpx_client(
        httpx.Client(
            base_url="https://example.test", transport=httpx.MockTransport(handler)
        )
    )
    workflow = ScientificRunsClient(generated)

    with pytest.raises(ApprovalRequiredError):
        workflow.run(
            {"capability_id": "external.write", "destination_project_id": "project_1"}
        )


def test_async_workflow_supports_resume_and_artifact_download():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/events/stream"):
            return httpx.Response(
                200,
                text=": no new events\n\n",
                headers={"content-type": "text/event-stream"},
            )
        if request.url.path == "/api/v1/jobs/job_1":
            return httpx.Response(200, json=_envelope(_job()))
        if request.url.path == "/api/v1/jobs/job_1/detail":
            return httpx.Response(200, json=_envelope({"artifacts": [_artifact()]}))
        if request.url.path == "/api/v1/artifacts/artifact_1/content":
            return httpx.Response(200, content=b"artifact")
        raise AssertionError(str(request.url))

    async def exercise() -> None:
        generated = AuthenticatedClient(base_url="https://example.test", token="token")
        generated.set_async_httpx_client(
            httpx.AsyncClient(
                base_url="https://example.test", transport=httpx.MockTransport(handler)
            )
        )
        workflow = AsyncScientificRunsClient(generated)

        result = await workflow.resume("job_1", download_artifacts=True)

        assert result.jobs[0]["state"] == "succeeded"
        assert result.artifact_contents == {"artifact_1": b"artifact"}
        exact = await workflow.download_artifact_exact(
            {
                "id": "artifact_1",
                "size_bytes": len(b"artifact"),
                "checksum_hex": hashlib.sha256(b"artifact").hexdigest(),
            },
            max_bytes=1024,
        )
        assert exact == b"artifact"
        await generated.get_async_httpx_client().aclose()

    asyncio.run(exercise())


def test_async_workflow_reads_retryable_stream_error_before_polling_fallback():
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        if request.url.path.endswith("/events/stream"):
            return httpx.Response(
                503,
                json={
                    "error": {
                        "code": "CAPACITY_UNAVAILABLE",
                        "message": "stream temporarily unavailable",
                        "retryable": True,
                    }
                },
            )
        if request.url.path == "/api/v1/jobs/job_1":
            return httpx.Response(200, json=_envelope(_job()))
        raise AssertionError(str(request.url))

    async def exercise() -> None:
        generated = AuthenticatedClient(base_url="https://example.test", token="token")
        generated.set_async_httpx_client(
            httpx.AsyncClient(
                base_url="https://example.test", transport=httpx.MockTransport(handler)
            )
        )
        workflow = AsyncScientificRunsClient(generated)

        job = await workflow.wait_for_job("job_1")

        assert job["state"] == "succeeded"
        await generated.get_async_httpx_client().aclose()

    asyncio.run(exercise())
    assert calls == [
        "/api/v1/jobs/job_1/events/stream",
        "/api/v1/jobs/job_1",
    ]
