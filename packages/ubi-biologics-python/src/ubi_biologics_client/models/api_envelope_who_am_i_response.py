from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_envelope_who_am_i_response_links import (
        APIEnvelopeWhoAmIResponseLinks,
    )
    from ..models.response_meta import ResponseMeta
    from ..models.who_am_i_response import WhoAmIResponse


T = TypeVar("T", bound="APIEnvelopeWhoAmIResponse")


@_attrs_define
class APIEnvelopeWhoAmIResponse:
    """
    Attributes:
        data (WhoAmIResponse):
        meta (ResponseMeta):
        links (APIEnvelopeWhoAmIResponseLinks | Unset):
    """

    data: WhoAmIResponse
    meta: ResponseMeta
    links: APIEnvelopeWhoAmIResponseLinks | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

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
        from ..models.api_envelope_who_am_i_response_links import (
            APIEnvelopeWhoAmIResponseLinks,
        )
        from ..models.response_meta import ResponseMeta
        from ..models.who_am_i_response import WhoAmIResponse

        d = dict(src_dict)
        data = WhoAmIResponse.from_dict(d.pop("data"))

        meta = ResponseMeta.from_dict(d.pop("meta"))

        _links = d.pop("links", UNSET)
        links: APIEnvelopeWhoAmIResponseLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = APIEnvelopeWhoAmIResponseLinks.from_dict(_links)

        api_envelope_who_am_i_response = cls(
            data=data,
            meta=meta,
            links=links,
        )

        return api_envelope_who_am_i_response
