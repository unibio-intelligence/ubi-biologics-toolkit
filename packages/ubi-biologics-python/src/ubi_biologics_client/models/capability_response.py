from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.capability_response_approval_policy import (
    CapabilityResponseApprovalPolicy,
)
from ..models.side_effect_class import SideEffectClass

if TYPE_CHECKING:
    from ..models.capability_executor_response import CapabilityExecutorResponse
    from ..models.capability_input_role_response import CapabilityInputRoleResponse
    from ..models.capability_output_response import CapabilityOutputResponse
    from ..models.capability_response_limits import CapabilityResponseLimits
    from ..models.capability_response_parameters_schema import (
        CapabilityResponseParametersSchema,
    )
    from ..models.capability_row_scope_contract_response import (
        CapabilityRowScopeContractResponse,
    )
    from ..models.fixed_credit_price_response import FixedCreditPriceResponse
    from ..models.result_evidence_profile_response import ResultEvidenceProfileResponse


T = TypeVar("T", bound="CapabilityResponse")


@_attrs_define
class CapabilityResponse:
    """
    Attributes:
        approval_policy (CapabilityResponseApprovalPolicy):
        description (str):
        executor (CapabilityExecutorResponse): Scientist-safe scheduling characteristics for a governed capability.

            Native service coordinates, protocol fields, and health contracts belong to
            the restricted runtime registry. They must never be serialized through the
            authenticated scientist contract.
        href (str):
        id (str):
        input_roles (list[CapabilityInputRoleResponse]):
        limits (CapabilityResponseLimits):
        name (str):
        outputs (list[CapabilityOutputResponse]):
        parameters_schema (CapabilityResponseParametersSchema):
        pricing (FixedCreditPriceResponse): One simple, non-currency price known before a user action.
        recommended_views (list[str]):
        released (bool):
        required_scopes (list[str]):
        result_evidence (ResultEvidenceProfileResponse):
        row_scope_contract (CapabilityRowScopeContractResponse): Universal row/batch semantics derived from the
            executable capability contract.
        side_effect_class (SideEffectClass):
        status (str):
        tags (list[str]):
        tool_id (str):
        version (str):
    """

    approval_policy: CapabilityResponseApprovalPolicy
    description: str
    executor: CapabilityExecutorResponse
    href: str
    id: str
    input_roles: list[CapabilityInputRoleResponse]
    limits: CapabilityResponseLimits
    name: str
    outputs: list[CapabilityOutputResponse]
    parameters_schema: CapabilityResponseParametersSchema
    pricing: FixedCreditPriceResponse
    recommended_views: list[str]
    released: bool
    required_scopes: list[str]
    result_evidence: ResultEvidenceProfileResponse
    row_scope_contract: CapabilityRowScopeContractResponse
    side_effect_class: SideEffectClass
    status: str
    tags: list[str]
    tool_id: str
    version: str

    def to_dict(self) -> dict[str, Any]:
        approval_policy = self.approval_policy.value

        description = self.description

        executor = self.executor.to_dict()

        href = self.href

        id = self.id

        input_roles = []
        for input_roles_item_data in self.input_roles:
            input_roles_item = input_roles_item_data.to_dict()
            input_roles.append(input_roles_item)

        limits = self.limits.to_dict()

        name = self.name

        outputs = []
        for outputs_item_data in self.outputs:
            outputs_item = outputs_item_data.to_dict()
            outputs.append(outputs_item)

        parameters_schema = self.parameters_schema.to_dict()

        pricing = self.pricing.to_dict()

        recommended_views = self.recommended_views

        released = self.released

        required_scopes = self.required_scopes

        result_evidence = self.result_evidence.to_dict()

        row_scope_contract = self.row_scope_contract.to_dict()

        side_effect_class = self.side_effect_class.value

        status = self.status

        tags = self.tags

        tool_id = self.tool_id

        version = self.version

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "approval_policy": approval_policy,
                "description": description,
                "executor": executor,
                "href": href,
                "id": id,
                "input_roles": input_roles,
                "limits": limits,
                "name": name,
                "outputs": outputs,
                "parameters_schema": parameters_schema,
                "pricing": pricing,
                "recommended_views": recommended_views,
                "released": released,
                "required_scopes": required_scopes,
                "result_evidence": result_evidence,
                "row_scope_contract": row_scope_contract,
                "side_effect_class": side_effect_class,
                "status": status,
                "tags": tags,
                "tool_id": tool_id,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.capability_executor_response import CapabilityExecutorResponse
        from ..models.capability_input_role_response import CapabilityInputRoleResponse
        from ..models.capability_output_response import CapabilityOutputResponse
        from ..models.capability_response_limits import CapabilityResponseLimits
        from ..models.capability_response_parameters_schema import (
            CapabilityResponseParametersSchema,
        )
        from ..models.capability_row_scope_contract_response import (
            CapabilityRowScopeContractResponse,
        )
        from ..models.fixed_credit_price_response import FixedCreditPriceResponse
        from ..models.result_evidence_profile_response import (
            ResultEvidenceProfileResponse,
        )

        d = dict(src_dict)
        approval_policy = CapabilityResponseApprovalPolicy(d.pop("approval_policy"))

        description = d.pop("description")

        executor = CapabilityExecutorResponse.from_dict(d.pop("executor"))

        href = d.pop("href")

        id = d.pop("id")

        input_roles = []
        _input_roles = d.pop("input_roles")
        for input_roles_item_data in _input_roles:
            input_roles_item = CapabilityInputRoleResponse.from_dict(
                input_roles_item_data
            )

            input_roles.append(input_roles_item)

        limits = CapabilityResponseLimits.from_dict(d.pop("limits"))

        name = d.pop("name")

        outputs = []
        _outputs = d.pop("outputs")
        for outputs_item_data in _outputs:
            outputs_item = CapabilityOutputResponse.from_dict(outputs_item_data)

            outputs.append(outputs_item)

        parameters_schema = CapabilityResponseParametersSchema.from_dict(
            d.pop("parameters_schema")
        )

        pricing = FixedCreditPriceResponse.from_dict(d.pop("pricing"))

        recommended_views = cast(list[str], d.pop("recommended_views"))

        released = d.pop("released")

        required_scopes = cast(list[str], d.pop("required_scopes"))

        result_evidence = ResultEvidenceProfileResponse.from_dict(
            d.pop("result_evidence")
        )

        row_scope_contract = CapabilityRowScopeContractResponse.from_dict(
            d.pop("row_scope_contract")
        )

        side_effect_class = SideEffectClass(d.pop("side_effect_class"))

        status = d.pop("status")

        tags = cast(list[str], d.pop("tags"))

        tool_id = d.pop("tool_id")

        version = d.pop("version")

        capability_response = cls(
            approval_policy=approval_policy,
            description=description,
            executor=executor,
            href=href,
            id=id,
            input_roles=input_roles,
            limits=limits,
            name=name,
            outputs=outputs,
            parameters_schema=parameters_schema,
            pricing=pricing,
            recommended_views=recommended_views,
            released=released,
            required_scopes=required_scopes,
            result_evidence=result_evidence,
            row_scope_contract=row_scope_contract,
            side_effect_class=side_effect_class,
            status=status,
            tags=tags,
            tool_id=tool_id,
            version=version,
        )

        return capability_response
