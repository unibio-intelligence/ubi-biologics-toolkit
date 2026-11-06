from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_envelope_artifact_response_links import (
        APIEnvelopeArtifactResponseLinks,
    )
    from ..models.artifact_response import ArtifactResponse
    from ..models.response_meta import ResponseMeta


T = TypeVar("T", bound="APIEnvelopeArtifactResponse")


@_attrs_define
class APIEnvelopeArtifactResponse:
    """
    Attributes:
        data (ArtifactResponse):
        meta (ResponseMeta):
        links (APIEnvelopeArtifactResponseLinks | Unset):
    """

    data: ArtifactResponse
    meta: ResponseMeta
    links: APIEnvelopeArtifactResponseLinks | Unset = UNSET

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
        from ..models.api_envelope_artifact_response_links import (
            APIEnvelopeArtifactResponseLinks,
        )
        from ..models.artifact_response import ArtifactResponse
        from ..models.response_meta import ResponseMeta

        d = dict(src_dict)
        data = ArtifactResponse.from_dict(d.pop("data"))

        meta = ResponseMeta.from_dict(d.pop("meta"))

        _links = d.pop("links", UNSET)
        links: APIEnvelopeArtifactResponseLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = APIEnvelopeArtifactResponseLinks.from_dict(_links)

        api_envelope_artifact_response = cls(
            data=data,
            meta=meta,
            links=links,
        )

        return api_envelope_artifact_response
