from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_envelopelist_project_response_links import (
        APIEnvelopelistProjectResponseLinks,
    )
    from ..models.project_response import ProjectResponse
    from ..models.response_meta import ResponseMeta


T = TypeVar("T", bound="APIEnvelopelistProjectResponse")


@_attrs_define
class APIEnvelopelistProjectResponse:
    """
    Attributes:
        data (list[ProjectResponse]):
        meta (ResponseMeta):
        links (APIEnvelopelistProjectResponseLinks | Unset):
    """

    data: list[ProjectResponse]
    meta: ResponseMeta
    links: APIEnvelopelistProjectResponseLinks | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        meta = self.meta.to_dict()

        links: dict[str, Any] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
                "meta": meta,
            }
        )
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_envelopelist_project_response_links import (
            APIEnvelopelistProjectResponseLinks,
        )
        from ..models.project_response import ProjectResponse
        from ..models.response_meta import ResponseMeta

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = ProjectResponse.from_dict(data_item_data)

            data.append(data_item)

        meta = ResponseMeta.from_dict(d.pop("meta"))

        _links = d.pop("links", UNSET)
        links: APIEnvelopelistProjectResponseLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = APIEnvelopelistProjectResponseLinks.from_dict(_links)

        api_envelopelist_project_response = cls(
            data=data,
            meta=meta,
            links=links,
        )

        return api_envelopelist_project_response
