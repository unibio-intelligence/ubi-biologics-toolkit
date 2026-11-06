from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_column_definition import DatasetColumnDefinition
    from ..models.dataset_row_input import DatasetRowInput


T = TypeVar("T", bound="DatasetVersionPublishRequest")


@_attrs_define
class DatasetVersionPublishRequest:
    """Publish a complete immutable successor snapshot.

    Callers send the complete desired snapshot rather than an in-place patch.  The
    service verifies the exact parent and Dataset revision before atomically moving
    the Dataset's current-version pointer.

        Attributes:
            columns (list[DatasetColumnDefinition]):
            creation_reason (str):
            expected_dataset_revision (int):
            parent_version_id (str):
            rows (list[DatasetRowInput]):
            run_id (None | str | Unset):
            source_asset_id (None | str | Unset):
    """

    columns: list[DatasetColumnDefinition]
    creation_reason: str
    expected_dataset_revision: int
    parent_version_id: str
    rows: list[DatasetRowInput]
    run_id: None | str | Unset = UNSET
    source_asset_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        columns = []
        for columns_item_data in self.columns:
            columns_item = columns_item_data.to_dict()
            columns.append(columns_item)

        creation_reason = self.creation_reason

        expected_dataset_revision = self.expected_dataset_revision

        parent_version_id = self.parent_version_id

        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data.to_dict()
            rows.append(rows_item)

        run_id: None | str | Unset
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        else:
            run_id = self.run_id

        source_asset_id: None | str | Unset
        if isinstance(self.source_asset_id, Unset):
            source_asset_id = UNSET
        else:
            source_asset_id = self.source_asset_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "columns": columns,
                "creation_reason": creation_reason,
                "expected_dataset_revision": expected_dataset_revision,
                "parent_version_id": parent_version_id,
                "rows": rows,
            }
        )
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
        if source_asset_id is not UNSET:
            field_dict["source_asset_id"] = source_asset_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_column_definition import DatasetColumnDefinition
        from ..models.dataset_row_input import DatasetRowInput

        d = dict(src_dict)
        columns = []
        _columns = d.pop("columns")
        for columns_item_data in _columns:
            columns_item = DatasetColumnDefinition.from_dict(columns_item_data)

            columns.append(columns_item)

        creation_reason = d.pop("creation_reason")

        expected_dataset_revision = d.pop("expected_dataset_revision")

        parent_version_id = d.pop("parent_version_id")

        rows = []
        _rows = d.pop("rows")
        for rows_item_data in _rows:
            rows_item = DatasetRowInput.from_dict(rows_item_data)

            rows.append(rows_item)

        def _parse_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        def _parse_source_asset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_asset_id = _parse_source_asset_id(d.pop("source_asset_id", UNSET))

        dataset_version_publish_request = cls(
            columns=columns,
            creation_reason=creation_reason,
            expected_dataset_revision=expected_dataset_revision,
            parent_version_id=parent_version_id,
            rows=rows,
            run_id=run_id,
            source_asset_id=source_asset_id,
        )

        return dataset_version_publish_request
