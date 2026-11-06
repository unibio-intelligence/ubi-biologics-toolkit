from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.api_envelopelist_project_response import APIEnvelopelistProjectResponse
from ...models.error_envelope import ErrorEnvelope
from ...models.project_list_view import ProjectListView
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_archived: bool | Unset = False,
    view: ProjectListView | Unset = UNSET,
    limit: int | Unset = 100,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["include_archived"] = include_archived

    json_view: str | Unset = UNSET
    if not isinstance(view, Unset):
        json_view = view.value

    params["view"] = json_view

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/projects",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIEnvelopelistProjectResponse | ErrorEnvelope:
    if response.status_code == 200:
        response_200 = APIEnvelopelistProjectResponse.from_dict(response.json())

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
) -> Response[APIEnvelopelistProjectResponse | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    include_archived: bool | Unset = False,
    view: ProjectListView | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[APIEnvelopelistProjectResponse | ErrorEnvelope]:
    """List Projects

    Args:
        include_archived (bool | Unset):  Default: False.
        view (ProjectListView | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopelistProjectResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        include_archived=include_archived,
        view=view,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    include_archived: bool | Unset = False,
    view: ProjectListView | Unset = UNSET,
    limit: int | Unset = 100,
) -> APIEnvelopelistProjectResponse | ErrorEnvelope | None:
    """List Projects

    Args:
        include_archived (bool | Unset):  Default: False.
        view (ProjectListView | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopelistProjectResponse | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        include_archived=include_archived,
        view=view,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    include_archived: bool | Unset = False,
    view: ProjectListView | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[APIEnvelopelistProjectResponse | ErrorEnvelope]:
    """List Projects

    Args:
        include_archived (bool | Unset):  Default: False.
        view (ProjectListView | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIEnvelopelistProjectResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        include_archived=include_archived,
        view=view,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    include_archived: bool | Unset = False,
    view: ProjectListView | Unset = UNSET,
    limit: int | Unset = 100,
) -> APIEnvelopelistProjectResponse | ErrorEnvelope | None:
    """List Projects

    Args:
        include_archived (bool | Unset):  Default: False.
        view (ProjectListView | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIEnvelopelistProjectResponse | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            include_archived=include_archived,
            view=view,
            limit=limit,
        )
    ).parsed
