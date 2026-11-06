from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_envelope_dataset_response_links import (
        APIEnvelopeDatasetResponseLinks,
    )
    from ..models.dataset_response import DatasetResponse
    from ..models.response_meta import ResponseMeta


T = TypeVar("T", bound="APIEnvelopeDatasetResponse")


@_attrs_define
class APIEnvelopeDatasetResponse:
    """
    Attributes:
        data (DatasetResponse):
        meta (ResponseMeta):
        links (APIEnvelopeDatasetResponseLinks | Unset):
    """

    data: DatasetResponse
    meta: ResponseMeta
    links: APIEnvelopeDatasetResponseLinks | Unset = UNSET

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
        from ..models.api_envelope_dataset_response_links import (
            APIEnvelopeDatasetResponseLinks,
        )
        from ..models.dataset_response import DatasetResponse
        from ..models.response_meta import ResponseMeta

        d = dict(src_dict)
        data = DatasetResponse.from_dict(d.pop("data"))

        meta = ResponseMeta.from_dict(d.pop("meta"))

        _links = d.pop("links", UNSET)
        links: APIEnvelopeDatasetResponseLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = APIEnvelopeDatasetResponseLinks.from_dict(_links)

        api_envelope_dataset_response = cls(
            data=data,
            meta=meta,
            links=links,
        )

        return api_envelope_dataset_response
