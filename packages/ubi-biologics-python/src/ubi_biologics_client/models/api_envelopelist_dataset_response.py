from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_envelopelist_dataset_response_links import (
        APIEnvelopelistDatasetResponseLinks,
    )
    from ..models.dataset_response import DatasetResponse
    from ..models.response_meta import ResponseMeta


T = TypeVar("T", bound="APIEnvelopelistDatasetResponse")


@_attrs_define
class APIEnvelopelistDatasetResponse:
    """
    Attributes:
        data (list[DatasetResponse]):
        meta (ResponseMeta):
        links (APIEnvelopelistDatasetResponseLinks | Unset):
    """

    data: list[DatasetResponse]
    meta: ResponseMeta
    links: APIEnvelopelistDatasetResponseLinks | Unset = UNSET

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
        from ..models.api_envelopelist_dataset_response_links import (
            APIEnvelopelistDatasetResponseLinks,
        )
        from ..models.dataset_response import DatasetResponse
        from ..models.response_meta import ResponseMeta

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = DatasetResponse.from_dict(data_item_data)

            data.append(data_item)

        meta = ResponseMeta.from_dict(d.pop("meta"))

        _links = d.pop("links", UNSET)
        links: APIEnvelopelistDatasetResponseLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = APIEnvelopelistDatasetResponseLinks.from_dict(_links)

        api_envelopelist_dataset_response = cls(
            data=data,
            meta=meta,
            links=links,
        )

        return api_envelopelist_dataset_response
