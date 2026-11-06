from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_tag_filter import DatasetTagFilter
    from ..models.filter_expression import FilterExpression
    from ..models.sort_expression import SortExpression


T = TypeVar("T", bound="DatasetQueryRequest")


@_attrs_define
class DatasetQueryRequest:
    """
    Attributes:
        cursor (None | str | Unset):
        filter_ (FilterExpression | None | Unset):
        filter_source (None | str | Unset):
        limit (int | Unset):  Default: 100.
        projection (list[str] | Unset):
        row_ids (list[str] | None | Unset):
        selection_id (None | str | Unset):
        sort (list[SortExpression] | Unset):
        tag_filter (DatasetTagFilter | None | Unset):
    """

    cursor: None | str | Unset = UNSET
    filter_: FilterExpression | None | Unset = UNSET
    filter_source: None | str | Unset = UNSET
    limit: int | Unset = 100
    projection: list[str] | Unset = UNSET
    row_ids: list[str] | None | Unset = UNSET
    selection_id: None | str | Unset = UNSET
    sort: list[SortExpression] | Unset = UNSET
    tag_filter: DatasetTagFilter | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_tag_filter import DatasetTagFilter
        from ..models.filter_expression import FilterExpression

        cursor: None | str | Unset
        if isinstance(self.cursor, Unset):
            cursor = UNSET
        else:
            cursor = self.cursor

        filter_: dict[str, Any] | None | Unset
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        elif isinstance(self.filter_, FilterExpression):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_

        filter_source: None | str | Unset
        if isinstance(self.filter_source, Unset):
            filter_source = UNSET
        else:
            filter_source = self.filter_source

        limit = self.limit

        projection: list[str] | Unset = UNSET
        if not isinstance(self.projection, Unset):
            projection = self.projection

        row_ids: list[str] | None | Unset
        if isinstance(self.row_ids, Unset):
            row_ids = UNSET
        elif isinstance(self.row_ids, list):
            row_ids = self.row_ids

        else:
            row_ids = self.row_ids

        selection_id: None | str | Unset
        if isinstance(self.selection_id, Unset):
            selection_id = UNSET
        else:
            selection_id = self.selection_id

        sort: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sort, Unset):
            sort = []
            for sort_item_data in self.sort:
                sort_item = sort_item_data.to_dict()
                sort.append(sort_item)

        tag_filter: dict[str, Any] | None | Unset
        if isinstance(self.tag_filter, Unset):
            tag_filter = UNSET
        elif isinstance(self.tag_filter, DatasetTagFilter):
            tag_filter = self.tag_filter.to_dict()
        else:
            tag_filter = self.tag_filter

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if cursor is not UNSET:
            field_dict["cursor"] = cursor
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if filter_source is not UNSET:
            field_dict["filter_source"] = filter_source
        if limit is not UNSET:
            field_dict["limit"] = limit
        if projection is not UNSET:
            field_dict["projection"] = projection
        if row_ids is not UNSET:
            field_dict["row_ids"] = row_ids
        if selection_id is not UNSET:
            field_dict["selection_id"] = selection_id
        if sort is not UNSET:
            field_dict["sort"] = sort
        if tag_filter is not UNSET:
            field_dict["tag_filter"] = tag_filter

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_tag_filter import DatasetTagFilter
        from ..models.filter_expression import FilterExpression
        from ..models.sort_expression import SortExpression

        d = dict(src_dict)

        def _parse_cursor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cursor = _parse_cursor(d.pop("cursor", UNSET))

        def _parse_filter_(data: object) -> FilterExpression | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0 = FilterExpression.from_dict(data)

                return filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FilterExpression | None | Unset, data)

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        def _parse_filter_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filter_source = _parse_filter_source(d.pop("filter_source", UNSET))

        limit = d.pop("limit", UNSET)

        projection = cast(list[str], d.pop("projection", UNSET))

        def _parse_row_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                row_ids_type_0 = cast(list[str], data)

                return row_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        row_ids = _parse_row_ids(d.pop("row_ids", UNSET))

        def _parse_selection_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        selection_id = _parse_selection_id(d.pop("selection_id", UNSET))

        _sort = d.pop("sort", UNSET)
        sort: list[SortExpression] | Unset = UNSET
        if _sort is not UNSET:
            sort = []
            for sort_item_data in _sort:
                sort_item = SortExpression.from_dict(sort_item_data)

                sort.append(sort_item)

        def _parse_tag_filter(data: object) -> DatasetTagFilter | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tag_filter_type_0 = DatasetTagFilter.from_dict(data)

                return tag_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DatasetTagFilter | None | Unset, data)

        tag_filter = _parse_tag_filter(d.pop("tag_filter", UNSET))

        dataset_query_request = cls(
            cursor=cursor,
            filter_=filter_,
            filter_source=filter_source,
            limit=limit,
            projection=projection,
            row_ids=row_ids,
            selection_id=selection_id,
            sort=sort,
            tag_filter=tag_filter,
        )

        return dataset_query_request
