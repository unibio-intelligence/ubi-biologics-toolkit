from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.api_envelope_dataset_query_response import (
    APIEnvelopeDatasetQueryResponse,
)
from ...models.dataset_query_request import DatasetQueryRequest
from ...models.error_envelope import ErrorEnvelope
from ...types import Response


def _get_kwargs(
    version_id: str,
    *,
    body: DatasetQueryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/dataset-versions/{version_id}/query".format(
            version_id=quote(str(version_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIEnvelopeDatasetQueryResponse | ErrorEnvelope:
    if response.status_code == 200:
        response_200 = APIEnvelopeDatasetQueryResponse.from_dict(response.json())

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
) -> Response[APIEnvelopeDatasetQueryResponse | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    version_id: str,
    *,
    client: AuthenticatedClient,
    body: DatasetQueryRequest,
) -> Response[APIEnvelopeDatasetQueryResponse | ErrorEnvelope]:
    """Query Dataset Version

    Args:
        version_id (str):
        body (DatasetQueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopeDatasetQueryResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        version_id=version_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    version_id: str,
    *,
    client: AuthenticatedClient,
    body: DatasetQueryRequest,
) -> APIEnvelopeDatasetQueryResponse | ErrorEnvelope | None:
    """Query Dataset Version

    Args:
        version_id (str):
        body (DatasetQueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopeDatasetQueryResponse | ErrorEnvelope
    """

    return sync_detailed(
        version_id=version_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    version_id: str,
    *,
    client: AuthenticatedClient,
    body: DatasetQueryRequest,
) -> Response[APIEnvelopeDatasetQueryResponse | ErrorEnvelope]:
    """Query Dataset Version

    Args:
        version_id (str):
        body (DatasetQueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopeDatasetQueryResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        version_id=version_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    version_id: str,
    *,
    client: AuthenticatedClient,
    body: DatasetQueryRequest,
) -> APIEnvelopeDatasetQueryResponse | ErrorEnvelope | None:
    """Query Dataset Version

    Args:
        version_id (str):
        body (DatasetQueryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopeDatasetQueryResponse | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            version_id=version_id,
            client=client,
            body=body,
        )
    ).parsed
