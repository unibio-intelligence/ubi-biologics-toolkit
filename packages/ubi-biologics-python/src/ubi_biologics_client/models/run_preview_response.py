from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.side_effect_class import SideEffectClass
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.capability_output_response import CapabilityOutputResponse
    from ..models.fixed_credit_price_response import FixedCreditPriceResponse
    from ..models.input_binding import InputBinding
    from ..models.run_preview_response_estimates import RunPreviewResponseEstimates
    from ..models.run_preview_response_normalized_parameters import (
        RunPreviewResponseNormalizedParameters,
    )
    from ..models.run_preview_response_policy import RunPreviewResponsePolicy
    from ..models.run_preview_response_warnings_item import (
        RunPreviewResponseWarningsItem,
    )


T = TypeVar("T", bound="RunPreviewResponse")


@_attrs_define
class RunPreviewResponse:
    """
    Attributes:
        approval_required (bool):
        binding_digest (str):
        capability_id (str):
        capability_version (str):
        estimates (RunPreviewResponseEstimates):
        expected_outputs (list[CapabilityOutputResponse]):
        normalized_inputs (list[InputBinding]):
        normalized_parameters (RunPreviewResponseNormalizedParameters):
        policy (RunPreviewResponsePolicy):
        preview_digest (str):
        pricing (FixedCreditPriceResponse): One simple, non-currency price known before a user action.
        side_effect_class (SideEffectClass):
        valid (bool):
        workbench_href (str):
        preview_receipt (None | str | Unset):
        preview_receipt_expires_at (None | str | Unset):
        warnings (list[RunPreviewResponseWarningsItem] | Unset):
    """

    approval_required: bool
    binding_digest: str
    capability_id: str
    capability_version: str
    estimates: RunPreviewResponseEstimates
    expected_outputs: list[CapabilityOutputResponse]
    normalized_inputs: list[InputBinding]
    normalized_parameters: RunPreviewResponseNormalizedParameters
    policy: RunPreviewResponsePolicy
    preview_digest: str
    pricing: FixedCreditPriceResponse
    side_effect_class: SideEffectClass
    valid: bool
    workbench_href: str
    preview_receipt: None | str | Unset = UNSET
    preview_receipt_expires_at: None | str | Unset = UNSET
    warnings: list[RunPreviewResponseWarningsItem] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        approval_required = self.approval_required

        binding_digest = self.binding_digest

        capability_id = self.capability_id

        capability_version = self.capability_version

        estimates = self.estimates.to_dict()

        expected_outputs = []
        for expected_outputs_item_data in self.expected_outputs:
            expected_outputs_item = expected_outputs_item_data.to_dict()
            expected_outputs.append(expected_outputs_item)

        normalized_inputs = []
        for normalized_inputs_item_data in self.normalized_inputs:
            normalized_inputs_item = normalized_inputs_item_data.to_dict()
            normalized_inputs.append(normalized_inputs_item)

        normalized_parameters = self.normalized_parameters.to_dict()

        policy = self.policy.to_dict()

        preview_digest = self.preview_digest

        pricing = self.pricing.to_dict()

        side_effect_class = self.side_effect_class.value

        valid = self.valid

        workbench_href = self.workbench_href

        preview_receipt: None | str | Unset
        if isinstance(self.preview_receipt, Unset):
            preview_receipt = UNSET
        else:
            preview_receipt = self.preview_receipt

        preview_receipt_expires_at: None | str | Unset
        if isinstance(self.preview_receipt_expires_at, Unset):
            preview_receipt_expires_at = UNSET
        else:
            preview_receipt_expires_at = self.preview_receipt_expires_at

        warnings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = []
            for warnings_item_data in self.warnings:
                warnings_item = warnings_item_data.to_dict()
                warnings.append(warnings_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "approval_required": approval_required,
                "binding_digest": binding_digest,
                "capability_id": capability_id,
                "capability_version": capability_version,
                "estimates": estimates,
                "expected_outputs": expected_outputs,
                "normalized_inputs": normalized_inputs,
                "normalized_parameters": normalized_parameters,
                "policy": policy,
                "preview_digest": preview_digest,
                "pricing": pricing,
                "side_effect_class": side_effect_class,
                "valid": valid,
                "workbench_href": workbench_href,
            }
        )
        if preview_receipt is not UNSET:
            field_dict["preview_receipt"] = preview_receipt
        if preview_receipt_expires_at is not UNSET:
            field_dict["preview_receipt_expires_at"] = preview_receipt_expires_at
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.capability_output_response import CapabilityOutputResponse
        from ..models.fixed_credit_price_response import FixedCreditPriceResponse
        from ..models.input_binding import InputBinding
        from ..models.run_preview_response_estimates import RunPreviewResponseEstimates
        from ..models.run_preview_response_normalized_parameters import (
            RunPreviewResponseNormalizedParameters,
        )
        from ..models.run_preview_response_policy import RunPreviewResponsePolicy
        from ..models.run_preview_response_warnings_item import (
            RunPreviewResponseWarningsItem,
        )

        d = dict(src_dict)
        approval_required = d.pop("approval_required")

        binding_digest = d.pop("binding_digest")

        capability_id = d.pop("capability_id")

        capability_version = d.pop("capability_version")

        estimates = RunPreviewResponseEstimates.from_dict(d.pop("estimates"))

        expected_outputs = []
        _expected_outputs = d.pop("expected_outputs")
        for expected_outputs_item_data in _expected_outputs:
            expected_outputs_item = CapabilityOutputResponse.from_dict(
                expected_outputs_item_data
            )

            expected_outputs.append(expected_outputs_item)

        normalized_inputs = []
        _normalized_inputs = d.pop("normalized_inputs")
        for normalized_inputs_item_data in _normalized_inputs:
            normalized_inputs_item = InputBinding.from_dict(normalized_inputs_item_data)

            normalized_inputs.append(normalized_inputs_item)

        normalized_parameters = RunPreviewResponseNormalizedParameters.from_dict(
            d.pop("normalized_parameters")
        )

        policy = RunPreviewResponsePolicy.from_dict(d.pop("policy"))

        preview_digest = d.pop("preview_digest")

        pricing = FixedCreditPriceResponse.from_dict(d.pop("pricing"))

        side_effect_class = SideEffectClass(d.pop("side_effect_class"))

        valid = d.pop("valid")

        workbench_href = d.pop("workbench_href")

        def _parse_preview_receipt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        preview_receipt = _parse_preview_receipt(d.pop("preview_receipt", UNSET))

        def _parse_preview_receipt_expires_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        preview_receipt_expires_at = _parse_preview_receipt_expires_at(
            d.pop("preview_receipt_expires_at", UNSET)
        )

        _warnings = d.pop("warnings", UNSET)
        warnings: list[RunPreviewResponseWarningsItem] | Unset = UNSET
        if _warnings is not UNSET:
            warnings = []
            for warnings_item_data in _warnings:
                warnings_item = RunPreviewResponseWarningsItem.from_dict(
                    warnings_item_data
                )

                warnings.append(warnings_item)

        run_preview_response = cls(
            approval_required=approval_required,
            binding_digest=binding_digest,
            capability_id=capability_id,
            capability_version=capability_version,
            estimates=estimates,
            expected_outputs=expected_outputs,
            normalized_inputs=normalized_inputs,
            normalized_parameters=normalized_parameters,
            policy=policy,
            preview_digest=preview_digest,
            pricing=pricing,
            side_effect_class=side_effect_class,
            valid=valid,
            workbench_href=workbench_href,
            preview_receipt=preview_receipt,
            preview_receipt_expires_at=preview_receipt_expires_at,
            warnings=warnings,
        )

        return run_preview_response
