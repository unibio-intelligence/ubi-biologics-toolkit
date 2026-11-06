from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    job_id: str,
    *,
    after_sequence: int | Unset = 0,
    timeout_seconds: int | Unset = 30,
    last_event_id: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(last_event_id, Unset):
        headers["Last-Event-ID"] = last_event_id

    params: dict[str, Any] = {}

    params["after_sequence"] = after_sequence

    params["timeout_seconds"] = timeout_seconds

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/jobs/{job_id}/events/stream".format(
            job_id=quote(str(job_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ErrorEnvelope:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 412:
        response_412 = ErrorEnvelope.from_dict(response.json())

        return response_412

    if response.status_code == 422:
        response_422 = ErrorEnvelope.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient,
    after_sequence: int | Unset = 0,
    timeout_seconds: int | Unset = 30,
    last_event_id: None | str | Unset = UNSET,
) -> Response[Any | ErrorEnvelope]:
    """Stream Job Events

    Args:
        job_id (str):
        after_sequence (int | Unset):  Default: 0.
        timeout_seconds (int | Unset):  Default: 30.
        last_event_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        after_sequence=after_sequence,
        timeout_seconds=timeout_seconds,
        last_event_id=last_event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: AuthenticatedClient,
    after_sequence: int | Unset = 0,
    timeout_seconds: int | Unset = 30,
    last_event_id: None | str | Unset = UNSET,
) -> Any | ErrorEnvelope | None:
    """Stream Job Events

    Args:
        job_id (str):
        after_sequence (int | Unset):  Default: 0.
        timeout_seconds (int | Unset):  Default: 30.
        last_event_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorEnvelope
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        after_sequence=after_sequence,
        timeout_seconds=timeout_seconds,
        last_event_id=last_event_id,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient,
    after_sequence: int | Unset = 0,
    timeout_seconds: int | Unset = 30,
    last_event_id: None | str | Unset = UNSET,
) -> Response[Any | ErrorEnvelope]:
    """Stream Job Events

    Args:
        job_id (str):
        after_sequence (int | Unset):  Default: 0.
        timeout_seconds (int | Unset):  Default: 30.
        last_event_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        after_sequence=after_sequence,
        timeout_seconds=timeout_seconds,
        last_event_id=last_event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: AuthenticatedClient,
    after_sequence: int | Unset = 0,
    timeout_seconds: int | Unset = 30,
    last_event_id: None | str | Unset = UNSET,
) -> Any | ErrorEnvelope | None:
    """Stream Job Events

    Args:
        job_id (str):
        after_sequence (int | Unset):  Default: 0.
        timeout_seconds (int | Unset):  Default: 30.
        last_event_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
            after_sequence=after_sequence,
            timeout_seconds=timeout_seconds,
            last_event_id=last_event_id,
        )
    ).parsed
