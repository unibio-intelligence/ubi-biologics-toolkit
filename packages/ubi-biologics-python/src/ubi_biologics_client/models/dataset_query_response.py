from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_column_response import DatasetColumnResponse
    from ..models.dataset_row_response import DatasetRowResponse


T = TypeVar("T", bound="DatasetQueryResponse")


@_attrs_define
class DatasetQueryResponse:
    """
    Attributes:
        columns (list[DatasetColumnResponse]):
        dataset_id (str):
        dataset_version_id (str):
        returned_count (int):
        rows (list[DatasetRowResponse]):
        total_count (int):
        truncated (bool):
        next_cursor (None | str | Unset):
    """

    columns: list[DatasetColumnResponse]
    dataset_id: str
    dataset_version_id: str
    returned_count: int
    rows: list[DatasetRowResponse]
    total_count: int
    truncated: bool
    next_cursor: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        columns = []
        for columns_item_data in self.columns:
            columns_item = columns_item_data.to_dict()
            columns.append(columns_item)

        dataset_id = self.dataset_id

        dataset_version_id = self.dataset_version_id

        returned_count = self.returned_count

        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data.to_dict()
            rows.append(rows_item)

        total_count = self.total_count

        truncated = self.truncated

        next_cursor: None | str | Unset
        if isinstance(self.next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "columns": columns,
                "dataset_id": dataset_id,
                "dataset_version_id": dataset_version_id,
                "returned_count": returned_count,
                "rows": rows,
                "total_count": total_count,
                "truncated": truncated,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_column_response import DatasetColumnResponse
        from ..models.dataset_row_response import DatasetRowResponse

        d = dict(src_dict)
        columns = []
        _columns = d.pop("columns")
        for columns_item_data in _columns:
            columns_item = DatasetColumnResponse.from_dict(columns_item_data)

            columns.append(columns_item)

        dataset_id = d.pop("dataset_id")

        dataset_version_id = d.pop("dataset_version_id")

        returned_count = d.pop("returned_count")

        rows = []
        _rows = d.pop("rows")
        for rows_item_data in _rows:
            rows_item = DatasetRowResponse.from_dict(rows_item_data)

            rows.append(rows_item)

        total_count = d.pop("total_count")

        truncated = d.pop("truncated")

        def _parse_next_cursor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor", UNSET))

        dataset_query_response = cls(
            columns=columns,
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
            returned_count=returned_count,
            rows=rows,
            total_count=total_count,
            truncated=truncated,
            next_cursor=next_cursor,
        )

        return dataset_query_response
