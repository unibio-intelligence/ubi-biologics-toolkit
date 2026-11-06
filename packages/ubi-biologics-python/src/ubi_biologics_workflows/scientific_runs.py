"""Governed preview, submission, Job waiting, and Artifact retrieval helpers.

This module deliberately calls only the canonical ``/api/v1`` contracts.  The
generated client remains the low-level contract; these clients add orchestration
without creating another execution path.
"""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import random as random_module
import time
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, TypeVar
from urllib.parse import quote
from uuid import uuid4

import httpx

from ubi_biologics_client import AuthenticatedClient


JsonObject = dict[str, Any]
TERMINAL_STATES = frozenset(
    {"succeeded", "failed", "cancelled", "timed_out", "expired"}
)
FAILURE_STATES = TERMINAL_STATES - {"succeeded"}
T = TypeVar("T")


class ScientificRunError(RuntimeError):
    """Base error carrying stable API diagnostics where available."""

    def __init__(
        self,
        message: str,
        *,
        code: str,
        status_code: int | None = None,
        retryable: bool = False,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.retryable = retryable
        self.details = dict(details or {})


class AdmissionError(ScientificRunError):
    """Preview, entitlement, quota, approval, or submission was refused."""


class ApprovalRequiredError(AdmissionError):
    """The digest-bound preview requires the platform approval workflow."""


class ExecutionError(ScientificRunError):
    """A durable Job reached a non-success terminal state."""


class PublicationError(ScientificRunError):
    """Execution finished, but governed outputs could not be published/read."""


class WorkflowTimeoutError(ScientificRunError):
    """The caller's local wait deadline elapsed; the durable Job continues."""


class WorkflowCancelledError(ScientificRunError):
    """The local wait was cancelled; this does not cancel the durable Job."""


class _SSEUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class ScientificRunResult:
    """Terminal governed result and its exact Job-scoped Artifacts."""

    preview: Mapping[str, Any] | None
    submission: Mapping[str, Any] | None
    jobs: tuple[Mapping[str, Any], ...]
    artifacts: tuple[Mapping[str, Any], ...]
    artifact_contents: Mapping[str, bytes] = field(default_factory=dict)


def _data(payload: object) -> JsonObject:
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), dict):
        raise ScientificRunError(
            "The API returned an invalid success envelope.",
            code="INVALID_API_ENVELOPE",
        )
    return dict(payload["data"])


def _retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return max(0.0, (parsed - datetime.now(timezone.utc)).total_seconds())
        except (TypeError, ValueError, OverflowError):
            return None


def _api_error(response: httpx.Response, *, admission: bool) -> ScientificRunError:
    try:
        payload = response.json()
    except ValueError:
        payload = {}
    body = payload.get("error", {}) if isinstance(payload, dict) else {}
    if not isinstance(body, dict):
        body = {}
    error_type: type[ScientificRunError] = (
        AdmissionError if admission else ScientificRunError
    )
    code = str(body.get("code") or f"HTTP_{response.status_code}")
    if code == "APPROVAL_REQUIRED":
        error_type = ApprovalRequiredError
    details = body.get("details")
    return error_type(
        str(
            body.get("message")
            or f"API request failed with HTTP {response.status_code}."
        ),
        code=code,
        status_code=response.status_code,
        retryable=bool(body.get("retryable")) or response.status_code in {429, 503},
        details=details if isinstance(details, dict) else None,
    )


def _raise_for_response(response: httpx.Response, *, admission: bool) -> None:
    if not response.is_success:
        raise _api_error(response, admission=admission)


def _check_cancelled(cancelled: Callable[[], bool] | None) -> None:
    if cancelled is not None and cancelled():
        raise WorkflowCancelledError(
            "The local wait was cancelled; the durable Job was not cancelled.",
            code="LOCAL_WAIT_CANCELLED",
        )


def _check_deadline(deadline: float, clock: Callable[[], float]) -> None:
    if clock() >= deadline:
        raise WorkflowTimeoutError(
            "Timed out waiting for the durable Job. Resume later with its Job ID.",
            code="LOCAL_WAIT_TIMEOUT",
            retryable=True,
        )


def _terminal_or_raise(job: JsonObject) -> bool:
    state = str(job.get("state", ""))
    if state not in TERMINAL_STATES:
        return False
    if state in FAILURE_STATES:
        raise ExecutionError(
            f"Job {job.get('id', '')} ended in state {state}.",
            code=f"JOB_{state.upper()}",
            details={"job": job},
        )
    if job.get("publication_state") != "published":
        raise PublicationError(
            f"Job {job.get('id', '')} succeeded without published outputs.",
            code="JOB_PUBLICATION_INCOMPLETE",
            details={"job": job},
        )
    return True


def _sse_events(lines: list[str]) -> list[JsonObject]:
    events: list[JsonObject] = []
    data_lines: list[str] = []
    for line in [*lines, ""]:
        if line == "":
            if data_lines:
                try:
                    import json

                    payload = json.loads("\n".join(data_lines))
                except (ValueError, TypeError):
                    payload = None
                if isinstance(payload, dict):
                    events.append(payload)
            data_lines = []
        elif line.startswith("data:"):
            data_lines.append(line[5:].lstrip())
    return events


class ScientificRunsClient:
    """Synchronous governed scientific execution workflow."""

    def __init__(
        self,
        client: AuthenticatedClient,
        *,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        random: Callable[[], float] = random_module.random,
    ) -> None:
        self.client = client
        self._sleep = sleep
        self._clock = clock
        self._random = random
        self._default_project_id: str | None = None
        self._default_project_key = str(uuid4())

    def ensure_default_project(self) -> str:
        if self._default_project_id:
            return self._default_project_id
        response = self.client.get_httpx_client().post(
            "/api/v1/projects/default",
            headers={"Idempotency-Key": self._default_project_key},
        )
        _raise_for_response(response, admission=True)
        project_id = _data(response.json()).get("id")
        if not isinstance(project_id, str) or not project_id:
            raise ScientificRunError(
                "Default Project response did not contain an ID.",
                code="INVALID_DEFAULT_PROJECT_RESPONSE",
            )
        self._default_project_id = project_id
        return project_id

    def _body(self, draft: Mapping[str, Any], *, mode: str) -> JsonObject:
        body = dict(draft)
        body["destination_project_id"] = (
            body.get("destination_project_id") or self.ensure_default_project()
        )
        body["inputs"] = list(body.get("inputs") or [])
        body["parameters"] = dict(body.get("parameters") or {})
        body["mode"] = mode
        return body

    def preview(self, draft: Mapping[str, Any]) -> JsonObject:
        response = self.client.get_httpx_client().post(
            "/api/v1/runs/preview", json=self._body(draft, mode="preview")
        )
        _raise_for_response(response, admission=True)
        return _data(response.json())

    def submit(
        self,
        draft: Mapping[str, Any],
        *,
        expected_preview_digest: str,
        preview_receipt: str,
        idempotency_key: str,
    ) -> JsonObject:
        body = self._body(draft, mode="execute")
        body["expected_preview_digest"] = expected_preview_digest
        body["preview_receipt"] = preview_receipt
        response = self.client.get_httpx_client().post(
            "/api/v1/runs",
            json=body,
            headers={"Idempotency-Key": idempotency_key},
        )
        _raise_for_response(response, admission=True)
        return _data(response.json())

    def _submit_with_retry(
        self,
        draft: Mapping[str, Any],
        *,
        preview_digest: str,
        preview_receipt: str,
        idempotency_key: str,
        attempts: int,
        deadline: float,
        cancelled: Callable[[], bool] | None,
    ) -> JsonObject:
        last_error: BaseException | None = None
        for attempt in range(attempts):
            _check_cancelled(cancelled)
            _check_deadline(deadline, self._clock)
            try:
                return self.submit(
                    draft,
                    expected_preview_digest=preview_digest,
                    preview_receipt=preview_receipt,
                    idempotency_key=idempotency_key,
                )
            except (httpx.TransportError, ScientificRunError) as exc:
                last_error = exc
                retryable = isinstance(exc, httpx.TransportError) or exc.retryable
                if not retryable or attempt + 1 >= attempts:
                    raise
                self._sleep(min(4.0, 0.25 * (2**attempt)))
        assert last_error is not None
        raise last_error

    def get_job(self, job_id: str) -> tuple[JsonObject, float | None]:
        response = self.client.get_httpx_client().get(
            f"/api/v1/jobs/{quote(job_id, safe='')}"
        )
        _raise_for_response(response, admission=False)
        return _data(response.json()), _retry_after_seconds(
            response.headers.get("Retry-After")
        )

    def _stream_once(
        self,
        job_id: str,
        *,
        after_sequence: int,
        timeout_seconds: int,
    ) -> list[JsonObject]:
        with self.client.get_httpx_client().stream(
            "GET",
            f"/api/v1/jobs/{quote(job_id, safe='')}/events/stream",
            params={
                "after_sequence": after_sequence,
                "timeout_seconds": timeout_seconds,
            },
            headers={"Accept": "text/event-stream"},
        ) as response:
            if not response.is_success:
                response.read()
            _raise_for_response(response, admission=False)
            if "text/event-stream" not in response.headers.get("content-type", ""):
                raise _SSEUnavailable("Job event endpoint did not return SSE.")
            return _sse_events(list(response.iter_lines()))

    def wait_for_job(
        self,
        job_id: str,
        *,
        timeout: float = 3600,
        cancelled: Callable[[], bool] | None = None,
        on_event: Callable[[Mapping[str, Any]], None] | None = None,
        on_state_change: Callable[[Mapping[str, Any]], None] | None = None,
        use_sse: bool = True,
        initial_poll_interval: float = 0.5,
        max_poll_interval: float = 8.0,
    ) -> JsonObject:
        deadline = self._clock() + timeout
        sequence = 0
        poll_attempt = 0
        stream_enabled = use_sse
        last_state: str | None = None
        while True:
            _check_cancelled(cancelled)
            _check_deadline(deadline, self._clock)
            if stream_enabled:
                try:
                    remaining = max(1, min(30, int(deadline - self._clock())))
                    events = self._stream_once(
                        job_id,
                        after_sequence=sequence,
                        timeout_seconds=remaining,
                    )
                    for event in events:
                        event_sequence = event.get("sequence")
                        if isinstance(event_sequence, int):
                            sequence = max(sequence, event_sequence)
                        if on_event:
                            on_event(event)
                except (_SSEUnavailable, httpx.TransportError):
                    stream_enabled = False
                except ScientificRunError as exc:
                    if exc.retryable:
                        stream_enabled = False
                    else:
                        raise

            job, retry_after = self.get_job(job_id)
            state = str(job.get("state", ""))
            if state != last_state:
                last_state = state
                if on_state_change:
                    on_state_change(job)
            if _terminal_or_raise(job):
                return job
            delay = retry_after
            if delay is None:
                delay = min(
                    max_poll_interval, initial_poll_interval * (2**poll_attempt)
                )
                delay *= 0.75 + (self._random() * 0.5)
            poll_attempt += 1
            self._sleep(min(delay, max(0.0, deadline - self._clock())))

    def _job_detail(self, job_id: str) -> JsonObject:
        response = self.client.get_httpx_client().get(
            f"/api/v1/jobs/{quote(job_id, safe='')}/detail"
        )
        if not response.is_success:
            error = _api_error(response, admission=False)
            raise PublicationError(
                str(error),
                code=error.code,
                status_code=error.status_code,
                retryable=error.retryable,
                details=error.details,
            ) from error
        return _data(response.json())

    def download_artifact(self, artifact_id: str) -> bytes:
        response = self.client.get_httpx_client().get(
            f"/api/v1/artifacts/{quote(artifact_id, safe='')}/content"
        )
        if not response.is_success:
            raise PublicationError(
                str(_api_error(response, admission=False)),
                code="ARTIFACT_DOWNLOAD_FAILED",
                status_code=response.status_code,
            )
        return response.content

    def download_artifact_exact(
        self,
        artifact: Mapping[str, Any],
        *,
        max_bytes: int,
    ) -> bytes:
        """Download one Artifact under a byte ceiling and verify its metadata.

        The Artifact detail response is the authority for the expected size and
        SHA-256.  Content is streamed so an incorrect or hostile response cannot
        make the workflow buffer more than ``max_bytes``.
        """

        artifact_id = artifact.get("id")
        expected_size = artifact.get("size_bytes")
        expected_checksum = artifact.get("checksum_hex")
        if (
            not isinstance(artifact_id, str)
            or not artifact_id
            or not isinstance(expected_size, int)
            or isinstance(expected_size, bool)
            or expected_size < 0
            or not isinstance(expected_checksum, str)
            or len(expected_checksum) != 64
            or any(
                character not in "0123456789abcdef" for character in expected_checksum
            )
            or not isinstance(max_bytes, int)
            or isinstance(max_bytes, bool)
            or max_bytes < 1
        ):
            raise PublicationError(
                "Artifact metadata or the download byte ceiling is invalid.",
                code="ARTIFACT_METADATA_INVALID",
            )
        if expected_size > max_bytes:
            raise PublicationError(
                f"Artifact {artifact_id} exceeds the configured download byte ceiling.",
                code="ARTIFACT_TOO_LARGE",
                details={"artifact_id": artifact_id, "max_bytes": max_bytes},
            )

        content = bytearray()
        digest = hashlib.sha256()
        with self.client.get_httpx_client().stream(
            "GET", f"/api/v1/artifacts/{quote(artifact_id, safe='')}/content"
        ) as response:
            if not response.is_success:
                raise PublicationError(
                    str(_api_error(response, admission=False)),
                    code="ARTIFACT_DOWNLOAD_FAILED",
                    status_code=response.status_code,
                )
            content_length = response.headers.get("Content-Length")
            if content_length is not None:
                try:
                    declared_size = int(content_length)
                except ValueError as exc:
                    raise PublicationError(
                        "Artifact response contained an invalid Content-Length.",
                        code="ARTIFACT_CONTENT_LENGTH_INVALID",
                    ) from exc
                if declared_size > max_bytes:
                    raise PublicationError(
                        f"Artifact {artifact_id} exceeds the configured download byte ceiling.",
                        code="ARTIFACT_TOO_LARGE",
                        details={"artifact_id": artifact_id, "max_bytes": max_bytes},
                    )
            for chunk in response.iter_bytes():
                if len(content) + len(chunk) > max_bytes:
                    raise PublicationError(
                        f"Artifact {artifact_id} exceeds the configured download byte ceiling.",
                        code="ARTIFACT_TOO_LARGE",
                        details={"artifact_id": artifact_id, "max_bytes": max_bytes},
                    )
                content.extend(chunk)
                digest.update(chunk)

        if len(content) != expected_size or digest.hexdigest() != expected_checksum:
            raise PublicationError(
                f"Artifact {artifact_id} content did not match its governed metadata.",
                code="ARTIFACT_INTEGRITY_MISMATCH",
                details={"artifact_id": artifact_id},
            )
        return bytes(content)

    def cancel(
        self,
        job_id: str,
        *,
        reason: str | None = None,
        idempotency_key: str | None = None,
    ) -> JsonObject:
        """Explicitly request durable server-side Job cancellation."""

        response = self.client.get_httpx_client().post(
            f"/api/v1/jobs/{quote(job_id, safe='')}/cancel",
            json={"reason": reason},
            headers={"Idempotency-Key": idempotency_key or str(uuid4())},
        )
        _raise_for_response(response, admission=False)
        return _data(response.json())

    def resume(
        self,
        job_id: str,
        *,
        timeout: float = 3600,
        cancelled: Callable[[], bool] | None = None,
        on_event: Callable[[Mapping[str, Any]], None] | None = None,
        on_state_change: Callable[[Mapping[str, Any]], None] | None = None,
        download_artifacts: bool = False,
        use_sse: bool = True,
    ) -> ScientificRunResult:
        job = self.wait_for_job(
            job_id,
            timeout=timeout,
            cancelled=cancelled,
            on_event=on_event,
            on_state_change=on_state_change,
            use_sse=use_sse,
        )
        detail = self._job_detail(job_id)
        artifacts = tuple(
            artifact
            for artifact in detail.get("artifacts", [])
            if isinstance(artifact, dict)
        )
        contents = (
            {
                str(artifact["id"]): self.download_artifact(str(artifact["id"]))
                for artifact in artifacts
                if isinstance(artifact.get("id"), str)
            }
            if download_artifacts
            else {}
        )
        return ScientificRunResult(
            preview=None,
            submission=None,
            jobs=(job,),
            artifacts=artifacts,
            artifact_contents=contents,
        )

    def run(
        self,
        draft: Mapping[str, Any],
        *,
        approve: Callable[[Mapping[str, Any]], bool | None] | None = None,
        on_submitted: Callable[[Mapping[str, Any]], None] | None = None,
        on_event: Callable[[Mapping[str, Any]], None] | None = None,
        on_state_change: Callable[[Mapping[str, Any]], None] | None = None,
        idempotency_key: str | None = None,
        timeout: float = 3600,
        cancelled: Callable[[], bool] | None = None,
        download_artifacts: bool = False,
        use_sse: bool = True,
        submission_attempts: int = 3,
    ) -> ScientificRunResult:
        deadline = self._clock() + timeout
        preview = self.preview(draft)
        if approve is not None and approve(preview) is False:
            raise AdmissionError(
                "The caller rejected the server-authored preview.",
                code="PREVIEW_REJECTED",
            )
        if preview.get("approval_required"):
            raise ApprovalRequiredError(
                "This preview requires the platform's digest-bound approval workflow.",
                code="APPROVAL_REQUIRED",
                details={"preview": preview},
            )
        preview_receipt = preview.get("preview_receipt")
        if not isinstance(preview_receipt, str) or not preview_receipt:
            raise AdmissionError(
                "The server preview did not include the required signed receipt.",
                code="PREVIEW_RECEIPT_REQUIRED",
            )
        key = idempotency_key or str(uuid4())
        submission = self._submit_with_retry(
            draft,
            preview_digest=str(preview["preview_digest"]),
            preview_receipt=preview_receipt,
            idempotency_key=key,
            attempts=max(1, submission_attempts),
            deadline=deadline,
            cancelled=cancelled,
        )
        if on_submitted:
            on_submitted(submission)
        jobs: list[Mapping[str, Any]] = []
        artifacts: list[Mapping[str, Any]] = []
        contents: dict[str, bytes] = {}
        for submitted_job in submission.get("jobs", []):
            if not isinstance(submitted_job, dict) or not isinstance(
                submitted_job.get("id"), str
            ):
                continue
            remaining = deadline - self._clock()
            result = self.resume(
                str(submitted_job["id"]),
                timeout=max(0.0, remaining),
                cancelled=cancelled,
                on_event=on_event,
                on_state_change=on_state_change,
                download_artifacts=download_artifacts,
                use_sse=use_sse,
            )
            jobs.extend(result.jobs)
            artifacts.extend(result.artifacts)
            contents.update(result.artifact_contents)
        if not jobs:
            raise ScientificRunError(
                "Run submission did not return a durable Job.",
                code="SUBMISSION_WITHOUT_JOB",
            )
        return ScientificRunResult(
            preview=preview,
            submission=submission,
            jobs=tuple(jobs),
            artifacts=tuple(artifacts),
            artifact_contents=contents,
        )


async def _maybe_await(value: T | Awaitable[T]) -> T:
    if inspect.isawaitable(value):
        return await value
    return value


class AsyncScientificRunsClient:
    """Asynchronous governed scientific execution workflow."""

    def __init__(
        self,
        client: AuthenticatedClient,
        *,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        clock: Callable[[], float] = time.monotonic,
        random: Callable[[], float] = random_module.random,
    ) -> None:
        self.client = client
        self._sleep = sleep
        self._clock = clock
        self._random = random
        self._default_project_id: str | None = None
        self._default_project_key = str(uuid4())
        self._default_project_lock = asyncio.Lock()

    async def ensure_default_project(self) -> str:
        if self._default_project_id:
            return self._default_project_id
        async with self._default_project_lock:
            if self._default_project_id:
                return self._default_project_id
            response = await self.client.get_async_httpx_client().post(
                "/api/v1/projects/default",
                headers={"Idempotency-Key": self._default_project_key},
            )
            _raise_for_response(response, admission=True)
            project_id = _data(response.json()).get("id")
            if not isinstance(project_id, str) or not project_id:
                raise ScientificRunError(
                    "Default Project response did not contain an ID.",
                    code="INVALID_DEFAULT_PROJECT_RESPONSE",
                )
            self._default_project_id = project_id
            return project_id

    async def _body(self, draft: Mapping[str, Any], *, mode: str) -> JsonObject:
        body = dict(draft)
        if not body.get("destination_project_id"):
            body["destination_project_id"] = await self.ensure_default_project()
        body["inputs"] = list(body.get("inputs") or [])
        body["parameters"] = dict(body.get("parameters") or {})
        body["mode"] = mode
        return body

    async def preview(self, draft: Mapping[str, Any]) -> JsonObject:
        response = await self.client.get_async_httpx_client().post(
            "/api/v1/runs/preview", json=await self._body(draft, mode="preview")
        )
        _raise_for_response(response, admission=True)
        return _data(response.json())

    async def submit(
        self,
        draft: Mapping[str, Any],
        *,
        expected_preview_digest: str,
        preview_receipt: str,
        idempotency_key: str,
    ) -> JsonObject:
        body = await self._body(draft, mode="execute")
        body["expected_preview_digest"] = expected_preview_digest
        body["preview_receipt"] = preview_receipt
        response = await self.client.get_async_httpx_client().post(
            "/api/v1/runs",
            json=body,
            headers={"Idempotency-Key": idempotency_key},
        )
        _raise_for_response(response, admission=True)
        return _data(response.json())

    async def _submit_with_retry(
        self,
        draft: Mapping[str, Any],
        *,
        preview_digest: str,
        preview_receipt: str,
        idempotency_key: str,
        attempts: int,
        deadline: float,
        cancelled: Callable[[], bool] | None,
    ) -> JsonObject:
        for attempt in range(attempts):
            _check_cancelled(cancelled)
            _check_deadline(deadline, self._clock)
            try:
                return await self.submit(
                    draft,
                    expected_preview_digest=preview_digest,
                    preview_receipt=preview_receipt,
                    idempotency_key=idempotency_key,
                )
            except (httpx.TransportError, ScientificRunError) as exc:
                retryable = isinstance(exc, httpx.TransportError) or exc.retryable
                if not retryable or attempt + 1 >= attempts:
                    raise
                await self._sleep(min(4.0, 0.25 * (2**attempt)))
        raise AssertionError("unreachable")

    async def get_job(self, job_id: str) -> tuple[JsonObject, float | None]:
        response = await self.client.get_async_httpx_client().get(
            f"/api/v1/jobs/{quote(job_id, safe='')}"
        )
        _raise_for_response(response, admission=False)
        return _data(response.json()), _retry_after_seconds(
            response.headers.get("Retry-After")
        )

    async def _stream_once(
        self,
        job_id: str,
        *,
        after_sequence: int,
        timeout_seconds: int,
    ) -> list[JsonObject]:
        async with self.client.get_async_httpx_client().stream(
            "GET",
            f"/api/v1/jobs/{quote(job_id, safe='')}/events/stream",
            params={
                "after_sequence": after_sequence,
                "timeout_seconds": timeout_seconds,
            },
            headers={"Accept": "text/event-stream"},
        ) as response:
            if not response.is_success:
                await response.aread()
            _raise_for_response(response, admission=False)
            if "text/event-stream" not in response.headers.get("content-type", ""):
                raise _SSEUnavailable("Job event endpoint did not return SSE.")
            return _sse_events([line async for line in response.aiter_lines()])

    async def wait_for_job(
        self,
        job_id: str,
        *,
        timeout: float = 3600,
        cancelled: Callable[[], bool] | None = None,
        on_event: Callable[[Mapping[str, Any]], Any | Awaitable[Any]] | None = None,
        on_state_change: (
            Callable[[Mapping[str, Any]], Any | Awaitable[Any]] | None
        ) = None,
        use_sse: bool = True,
        initial_poll_interval: float = 0.5,
        max_poll_interval: float = 8.0,
    ) -> JsonObject:
        deadline = self._clock() + timeout
        sequence = 0
        poll_attempt = 0
        stream_enabled = use_sse
        last_state: str | None = None
        while True:
            _check_cancelled(cancelled)
            _check_deadline(deadline, self._clock)
            if stream_enabled:
                try:
                    remaining = max(1, min(30, int(deadline - self._clock())))
                    events = await self._stream_once(
                        job_id,
                        after_sequence=sequence,
                        timeout_seconds=remaining,
                    )
                    for event in events:
                        event_sequence = event.get("sequence")
                        if isinstance(event_sequence, int):
                            sequence = max(sequence, event_sequence)
                        if on_event:
                            await _maybe_await(on_event(event))
                except (_SSEUnavailable, httpx.TransportError):
                    stream_enabled = False
                except ScientificRunError as exc:
                    if exc.retryable:
                        stream_enabled = False
                    else:
                        raise

            job, retry_after = await self.get_job(job_id)
            state = str(job.get("state", ""))
            if state != last_state:
                last_state = state
                if on_state_change:
                    await _maybe_await(on_state_change(job))
            if _terminal_or_raise(job):
                return job
            delay = retry_after
            if delay is None:
                delay = min(
                    max_poll_interval, initial_poll_interval * (2**poll_attempt)
                )
                delay *= 0.75 + (self._random() * 0.5)
            poll_attempt += 1
            await self._sleep(min(delay, max(0.0, deadline - self._clock())))

    async def _job_detail(self, job_id: str) -> JsonObject:
        response = await self.client.get_async_httpx_client().get(
            f"/api/v1/jobs/{quote(job_id, safe='')}/detail"
        )
        if not response.is_success:
            error = _api_error(response, admission=False)
            raise PublicationError(
                str(error),
                code=error.code,
                status_code=error.status_code,
                retryable=error.retryable,
                details=error.details,
            ) from error
        return _data(response.json())

    async def download_artifact(self, artifact_id: str) -> bytes:
        response = await self.client.get_async_httpx_client().get(
            f"/api/v1/artifacts/{quote(artifact_id, safe='')}/content"
        )
        if not response.is_success:
            raise PublicationError(
                str(_api_error(response, admission=False)),
                code="ARTIFACT_DOWNLOAD_FAILED",
                status_code=response.status_code,
            )
        return response.content

    async def download_artifact_exact(
        self,
        artifact: Mapping[str, Any],
        *,
        max_bytes: int,
    ) -> bytes:
        """Asynchronously download and verify one byte-bounded Artifact."""

        artifact_id = artifact.get("id")
        expected_size = artifact.get("size_bytes")
        expected_checksum = artifact.get("checksum_hex")
        if (
            not isinstance(artifact_id, str)
            or not artifact_id
            or not isinstance(expected_size, int)
            or isinstance(expected_size, bool)
            or expected_size < 0
            or not isinstance(expected_checksum, str)
            or len(expected_checksum) != 64
            or any(
                character not in "0123456789abcdef" for character in expected_checksum
            )
            or not isinstance(max_bytes, int)
            or isinstance(max_bytes, bool)
            or max_bytes < 1
        ):
            raise PublicationError(
                "Artifact metadata or the download byte ceiling is invalid.",
                code="ARTIFACT_METADATA_INVALID",
            )
        if expected_size > max_bytes:
            raise PublicationError(
                f"Artifact {artifact_id} exceeds the configured download byte ceiling.",
                code="ARTIFACT_TOO_LARGE",
                details={"artifact_id": artifact_id, "max_bytes": max_bytes},
            )

        content = bytearray()
        digest = hashlib.sha256()
        async with self.client.get_async_httpx_client().stream(
            "GET", f"/api/v1/artifacts/{quote(artifact_id, safe='')}/content"
        ) as response:
            if not response.is_success:
                raise PublicationError(
                    str(_api_error(response, admission=False)),
                    code="ARTIFACT_DOWNLOAD_FAILED",
                    status_code=response.status_code,
                )
            content_length = response.headers.get("Content-Length")
            if content_length is not None:
                try:
                    declared_size = int(content_length)
                except ValueError as exc:
                    raise PublicationError(
                        "Artifact response contained an invalid Content-Length.",
                        code="ARTIFACT_CONTENT_LENGTH_INVALID",
                    ) from exc
                if declared_size > max_bytes:
                    raise PublicationError(
                        f"Artifact {artifact_id} exceeds the configured download byte ceiling.",
                        code="ARTIFACT_TOO_LARGE",
                        details={"artifact_id": artifact_id, "max_bytes": max_bytes},
                    )
            async for chunk in response.aiter_bytes():
                if len(content) + len(chunk) > max_bytes:
                    raise PublicationError(
                        f"Artifact {artifact_id} exceeds the configured download byte ceiling.",
                        code="ARTIFACT_TOO_LARGE",
                        details={"artifact_id": artifact_id, "max_bytes": max_bytes},
                    )
                content.extend(chunk)
                digest.update(chunk)

        if len(content) != expected_size or digest.hexdigest() != expected_checksum:
            raise PublicationError(
                f"Artifact {artifact_id} content did not match its governed metadata.",
                code="ARTIFACT_INTEGRITY_MISMATCH",
                details={"artifact_id": artifact_id},
            )
        return bytes(content)

    async def cancel(
        self,
        job_id: str,
        *,
        reason: str | None = None,
        idempotency_key: str | None = None,
    ) -> JsonObject:
        """Explicitly request durable server-side Job cancellation."""

        response = await self.client.get_async_httpx_client().post(
            f"/api/v1/jobs/{quote(job_id, safe='')}/cancel",
            json={"reason": reason},
            headers={"Idempotency-Key": idempotency_key or str(uuid4())},
        )
        _raise_for_response(response, admission=False)
        return _data(response.json())

    async def resume(
        self,
        job_id: str,
        *,
        timeout: float = 3600,
        cancelled: Callable[[], bool] | None = None,
        on_event: Callable[[Mapping[str, Any]], Any | Awaitable[Any]] | None = None,
        on_state_change: (
            Callable[[Mapping[str, Any]], Any | Awaitable[Any]] | None
        ) = None,
        download_artifacts: bool = False,
        use_sse: bool = True,
    ) -> ScientificRunResult:
        job = await self.wait_for_job(
            job_id,
            timeout=timeout,
            cancelled=cancelled,
            on_event=on_event,
            on_state_change=on_state_change,
            use_sse=use_sse,
        )
        detail = await self._job_detail(job_id)
        artifacts = tuple(
            artifact
            for artifact in detail.get("artifacts", [])
            if isinstance(artifact, dict)
        )
        contents: dict[str, bytes] = {}
        if download_artifacts:
            pairs = await asyncio.gather(
                *(
                    self.download_artifact(str(artifact["id"]))
                    for artifact in artifacts
                    if isinstance(artifact.get("id"), str)
                )
            )
            ids = [
                str(artifact["id"])
                for artifact in artifacts
                if isinstance(artifact.get("id"), str)
            ]
            contents = dict(zip(ids, pairs, strict=True))
        return ScientificRunResult(
            preview=None,
            submission=None,
            jobs=(job,),
            artifacts=artifacts,
            artifact_contents=contents,
        )

    async def run(
        self,
        draft: Mapping[str, Any],
        *,
        approve: (
            Callable[[Mapping[str, Any]], bool | None | Awaitable[bool | None]] | None
        ) = None,
        on_submitted: Callable[[Mapping[str, Any]], Any | Awaitable[Any]] | None = None,
        on_event: Callable[[Mapping[str, Any]], Any | Awaitable[Any]] | None = None,
        on_state_change: (
            Callable[[Mapping[str, Any]], Any | Awaitable[Any]] | None
        ) = None,
        idempotency_key: str | None = None,
        timeout: float = 3600,
        cancelled: Callable[[], bool] | None = None,
        download_artifacts: bool = False,
        use_sse: bool = True,
        submission_attempts: int = 3,
    ) -> ScientificRunResult:
        deadline = self._clock() + timeout
        preview = await self.preview(draft)
        if approve is not None and await _maybe_await(approve(preview)) is False:
            raise AdmissionError(
                "The caller rejected the server-authored preview.",
                code="PREVIEW_REJECTED",
            )
        if preview.get("approval_required"):
            raise ApprovalRequiredError(
                "This preview requires the platform's digest-bound approval workflow.",
                code="APPROVAL_REQUIRED",
                details={"preview": preview},
            )
        preview_receipt = preview.get("preview_receipt")
        if not isinstance(preview_receipt, str) or not preview_receipt:
            raise AdmissionError(
                "The server preview did not include the required signed receipt.",
                code="PREVIEW_RECEIPT_REQUIRED",
            )
        key = idempotency_key or str(uuid4())
        submission = await self._submit_with_retry(
            draft,
            preview_digest=str(preview["preview_digest"]),
            preview_receipt=preview_receipt,
            idempotency_key=key,
            attempts=max(1, submission_attempts),
            deadline=deadline,
            cancelled=cancelled,
        )
        if on_submitted:
            await _maybe_await(on_submitted(submission))
        submitted_jobs = [
            job
            for job in submission.get("jobs", [])
            if isinstance(job, dict) and isinstance(job.get("id"), str)
        ]
        if not submitted_jobs:
            raise ScientificRunError(
                "Run submission did not return a durable Job.",
                code="SUBMISSION_WITHOUT_JOB",
            )

        async def finish(job: Mapping[str, Any]) -> ScientificRunResult:
            return await self.resume(
                str(job["id"]),
                timeout=max(0.0, deadline - self._clock()),
                cancelled=cancelled,
                on_event=on_event,
                on_state_change=on_state_change,
                download_artifacts=download_artifacts,
                use_sse=use_sse,
            )

        results = await asyncio.gather(*(finish(job) for job in submitted_jobs))
        return ScientificRunResult(
            preview=preview,
            submission=submission,
            jobs=tuple(job for result in results for job in result.jobs),
            artifacts=tuple(
                artifact for result in results for artifact in result.artifacts
            ),
            artifact_contents={
                artifact_id: content
                for result in results
                for artifact_id, content in result.artifact_contents.items()
            },
        )
