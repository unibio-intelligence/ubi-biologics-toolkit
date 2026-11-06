from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.api_envelope_dataset_response import APIEnvelopeDatasetResponse
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dataset_id: str,
    *,
    include_current_version: bool | Unset = True,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["include_current_version"] = include_current_version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/datasets/{dataset_id}".format(
            dataset_id=quote(str(dataset_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIEnvelopeDatasetResponse | ErrorEnvelope:
    if response.status_code == 200:
        response_200 = APIEnvelopeDatasetResponse.from_dict(response.json())

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
) -> Response[APIEnvelopeDatasetResponse | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    include_current_version: bool | Unset = True,
) -> Response[APIEnvelopeDatasetResponse | ErrorEnvelope]:
    """Get Dataset

    Args:
        dataset_id (str):
        include_current_version (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopeDatasetResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        include_current_version=include_current_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    include_current_version: bool | Unset = True,
) -> APIEnvelopeDatasetResponse | ErrorEnvelope | None:
    """Get Dataset

    Args:
        dataset_id (str):
        include_current_version (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopeDatasetResponse | ErrorEnvelope
    """

    return sync_detailed(
        dataset_id=dataset_id,
        client=client,
        include_current_version=include_current_version,
    ).parsed


async def asyncio_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    include_current_version: bool | Unset = True,
) -> Response[APIEnvelopeDatasetResponse | ErrorEnvelope]:
    """Get Dataset

    Args:
        dataset_id (str):
        include_current_version (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopeDatasetResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        include_current_version=include_current_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    include_current_version: bool | Unset = True,
) -> APIEnvelopeDatasetResponse | ErrorEnvelope | None:
    """Get Dataset

    Args:
        dataset_id (str):
        include_current_version (bool | Unset):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopeDatasetResponse | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            dataset_id=dataset_id,
            client=client,
            include_current_version=include_current_version,
        )
    ).parsed
