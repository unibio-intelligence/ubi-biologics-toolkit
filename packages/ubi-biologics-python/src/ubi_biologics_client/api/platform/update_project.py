from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.api_envelope_project_response import APIEnvelopeProjectResponse
from ...models.error_envelope import ErrorEnvelope
from ...models.project_update_request import ProjectUpdateRequest
from ...types import Response


def _get_kwargs(
    project_id: str,
    *,
    body: ProjectUpdateRequest,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/projects/{project_id}".format(
            project_id=quote(str(project_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIEnvelopeProjectResponse | ErrorEnvelope:
    if response.status_code == 200:
        response_200 = APIEnvelopeProjectResponse.from_dict(response.json())

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
) -> Response[APIEnvelopeProjectResponse | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: ProjectUpdateRequest,
    idempotency_key: str,
) -> Response[APIEnvelopeProjectResponse | ErrorEnvelope]:
    """Update Project

    Args:
        project_id (str):
        idempotency_key (str):
        body (ProjectUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopeProjectResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: ProjectUpdateRequest,
    idempotency_key: str,
) -> APIEnvelopeProjectResponse | ErrorEnvelope | None:
    """Update Project

    Args:
        project_id (str):
        idempotency_key (str):
        body (ProjectUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopeProjectResponse | ErrorEnvelope
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: ProjectUpdateRequest,
    idempotency_key: str,
) -> Response[APIEnvelopeProjectResponse | ErrorEnvelope]:
    """Update Project

    Args:
        project_id (str):
        idempotency_key (str):
        body (ProjectUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopeProjectResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: ProjectUpdateRequest,
    idempotency_key: str,
) -> APIEnvelopeProjectResponse | ErrorEnvelope | None:
    """Update Project

    Args:
        project_id (str):
        idempotency_key (str):
        body (ProjectUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopeProjectResponse | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
