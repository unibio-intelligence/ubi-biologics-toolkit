from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

from ..models.capability_row_scope_contract_response_accepted_selection_modes_item import (
    CapabilityRowScopeContractResponseAcceptedSelectionModesItem,
)
from ..models.capability_row_scope_contract_response_empty_scope_policy import (
    CapabilityRowScopeContractResponseEmptyScopePolicy,
)
from ..models.capability_row_scope_contract_response_operation_level import (
    CapabilityRowScopeContractResponseOperationLevel,
)
from ..models.capability_row_scope_contract_response_row_order import (
    CapabilityRowScopeContractResponseRowOrder,
)
from ..models.capability_row_scope_contract_response_scope_binding import (
    CapabilityRowScopeContractResponseScopeBinding,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CapabilityRowScopeContractResponse")


@_attrs_define
class CapabilityRowScopeContractResponse:
    """Universal row/batch semantics derived from the executable capability contract.

    Attributes:
        accepted_selection_modes (list[CapabilityRowScopeContractResponseAcceptedSelectionModesItem]):
        empty_scope_policy (CapabilityRowScopeContractResponseEmptyScopePolicy):
        execution_cardinality (Literal['one_run_per_exact_scope']):
        failure_semantics (Literal['capability_result_contract']):
        operation_level (CapabilityRowScopeContractResponseOperationLevel):
        row_order (CapabilityRowScopeContractResponseRowOrder):
        scope_binding (CapabilityRowScopeContractResponseScopeBinding):
        maximum_rows_per_native_batch (int | None | Unset):
        maximum_rows_per_run (int | None | Unset):
        minimum_rows_per_run (int | None | Unset):
    """

    accepted_selection_modes: list[
        CapabilityRowScopeContractResponseAcceptedSelectionModesItem
    ]
    empty_scope_policy: CapabilityRowScopeContractResponseEmptyScopePolicy
    execution_cardinality: Literal["one_run_per_exact_scope"]
    failure_semantics: Literal["capability_result_contract"]
    operation_level: CapabilityRowScopeContractResponseOperationLevel
    row_order: CapabilityRowScopeContractResponseRowOrder
    scope_binding: CapabilityRowScopeContractResponseScopeBinding
    maximum_rows_per_native_batch: int | None | Unset = UNSET
    maximum_rows_per_run: int | None | Unset = UNSET
    minimum_rows_per_run: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        accepted_selection_modes = []
        for accepted_selection_modes_item_data in self.accepted_selection_modes:
            accepted_selection_modes_item = accepted_selection_modes_item_data.value
            accepted_selection_modes.append(accepted_selection_modes_item)

        empty_scope_policy = self.empty_scope_policy.value

        execution_cardinality = self.execution_cardinality

        failure_semantics = self.failure_semantics

        operation_level = self.operation_level.value

        row_order = self.row_order.value

        scope_binding = self.scope_binding.value

        maximum_rows_per_native_batch: int | None | Unset
        if isinstance(self.maximum_rows_per_native_batch, Unset):
            maximum_rows_per_native_batch = UNSET
        else:
            maximum_rows_per_native_batch = self.maximum_rows_per_native_batch

        maximum_rows_per_run: int | None | Unset
        if isinstance(self.maximum_rows_per_run, Unset):
            maximum_rows_per_run = UNSET
        else:
            maximum_rows_per_run = self.maximum_rows_per_run

        minimum_rows_per_run: int | None | Unset
        if isinstance(self.minimum_rows_per_run, Unset):
            minimum_rows_per_run = UNSET
        else:
            minimum_rows_per_run = self.minimum_rows_per_run

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "accepted_selection_modes": accepted_selection_modes,
                "empty_scope_policy": empty_scope_policy,
                "execution_cardinality": execution_cardinality,
                "failure_semantics": failure_semantics,
                "operation_level": operation_level,
                "row_order": row_order,
                "scope_binding": scope_binding,
            }
        )
        if maximum_rows_per_native_batch is not UNSET:
            field_dict["maximum_rows_per_native_batch"] = maximum_rows_per_native_batch
        if maximum_rows_per_run is not UNSET:
            field_dict["maximum_rows_per_run"] = maximum_rows_per_run
        if minimum_rows_per_run is not UNSET:
            field_dict["minimum_rows_per_run"] = minimum_rows_per_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        accepted_selection_modes = []
        _accepted_selection_modes = d.pop("accepted_selection_modes")
        for accepted_selection_modes_item_data in _accepted_selection_modes:
            accepted_selection_modes_item = (
                CapabilityRowScopeContractResponseAcceptedSelectionModesItem(
                    accepted_selection_modes_item_data
                )
            )

            accepted_selection_modes.append(accepted_selection_modes_item)

        empty_scope_policy = CapabilityRowScopeContractResponseEmptyScopePolicy(
            d.pop("empty_scope_policy")
        )

        execution_cardinality = cast(
            Literal["one_run_per_exact_scope"], d.pop("execution_cardinality")
        )
        if execution_cardinality != "one_run_per_exact_scope":
            raise ValueError(
                f"execution_cardinality must match const 'one_run_per_exact_scope', got '{execution_cardinality}'"
            )

        failure_semantics = cast(
            Literal["capability_result_contract"], d.pop("failure_semantics")
        )
        if failure_semantics != "capability_result_contract":
            raise ValueError(
                f"failure_semantics must match const 'capability_result_contract', got '{failure_semantics}'"
            )

        operation_level = CapabilityRowScopeContractResponseOperationLevel(
            d.pop("operation_level")
        )

        row_order = CapabilityRowScopeContractResponseRowOrder(d.pop("row_order"))

        scope_binding = CapabilityRowScopeContractResponseScopeBinding(
            d.pop("scope_binding")
        )

        def _parse_maximum_rows_per_native_batch(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        maximum_rows_per_native_batch = _parse_maximum_rows_per_native_batch(
            d.pop("maximum_rows_per_native_batch", UNSET)
        )

        def _parse_maximum_rows_per_run(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        maximum_rows_per_run = _parse_maximum_rows_per_run(
            d.pop("maximum_rows_per_run", UNSET)
        )

        def _parse_minimum_rows_per_run(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        minimum_rows_per_run = _parse_minimum_rows_per_run(
            d.pop("minimum_rows_per_run", UNSET)
        )

        capability_row_scope_contract_response = cls(
            accepted_selection_modes=accepted_selection_modes,
            empty_scope_policy=empty_scope_policy,
            execution_cardinality=execution_cardinality,
            failure_semantics=failure_semantics,
            operation_level=operation_level,
            row_order=row_order,
            scope_binding=scope_binding,
            maximum_rows_per_native_batch=maximum_rows_per_native_batch,
            maximum_rows_per_run=maximum_rows_per_run,
            minimum_rows_per_run=minimum_rows_per_run,
        )

        return capability_row_scope_contract_response
