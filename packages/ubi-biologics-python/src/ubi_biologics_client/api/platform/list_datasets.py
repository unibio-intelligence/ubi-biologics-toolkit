from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.api_envelopelist_dataset_response import APIEnvelopelistDatasetResponse
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: str,
    limit: int | Unset = 50,
    include_current_version: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["project_id"] = project_id

    params["limit"] = limit

    params["include_current_version"] = include_current_version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/datasets",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIEnvelopelistDatasetResponse | ErrorEnvelope:
    if response.status_code == 200:
        response_200 = APIEnvelopelistDatasetResponse.from_dict(response.json())

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
) -> Response[APIEnvelopelistDatasetResponse | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id: str,
    limit: int | Unset = 50,
    include_current_version: bool | Unset = False,
) -> Response[APIEnvelopelistDatasetResponse | ErrorEnvelope]:
    """List Datasets

    Args:
        project_id (str):
        limit (int | Unset):  Default: 50.
        include_current_version (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopelistDatasetResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        limit=limit,
        include_current_version=include_current_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id: str,
    limit: int | Unset = 50,
    include_current_version: bool | Unset = False,
) -> APIEnvelopelistDatasetResponse | ErrorEnvelope | None:
    """List Datasets

    Args:
        project_id (str):
        limit (int | Unset):  Default: 50.
        include_current_version (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopelistDatasetResponse | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        limit=limit,
        include_current_version=include_current_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: str,
    limit: int | Unset = 50,
    include_current_version: bool | Unset = False,
) -> Response[APIEnvelopelistDatasetResponse | ErrorEnvelope]:
    """List Datasets

    Args:
        project_id (str):
        limit (int | Unset):  Default: 50.
        include_current_version (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopelistDatasetResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        limit=limit,
        include_current_version=include_current_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: str,
    limit: int | Unset = 50,
    include_current_version: bool | Unset = False,
) -> APIEnvelopelistDatasetResponse | ErrorEnvelope | None:
    """List Datasets

    Args:
        project_id (str):
        limit (int | Unset):  Default: 50.
        include_current_version (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopelistDatasetResponse | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            limit=limit,
            include_current_version=include_current_version,
        )
    ).parsed
