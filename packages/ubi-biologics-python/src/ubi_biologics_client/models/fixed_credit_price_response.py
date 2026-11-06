from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="FixedCreditPriceResponse")


@_attrs_define
class FixedCreditPriceResponse:
    """One simple, non-currency price known before a user action.

    Attributes:
        credit_cost (int):
        pricing_note (str):
        billing_unit (Literal['credits'] | Unset):  Default: 'credits'.
        pricing_model (Literal['ubi_fixed_operation_credits_v1'] | Unset):  Default: 'ubi_fixed_operation_credits_v1'.
    """

    credit_cost: int
    pricing_note: str
    billing_unit: Literal["credits"] | Unset = "credits"
    pricing_model: Literal["ubi_fixed_operation_credits_v1"] | Unset = (
        "ubi_fixed_operation_credits_v1"
    )

    def to_dict(self) -> dict[str, Any]:
        credit_cost = self.credit_cost

        pricing_note = self.pricing_note

        billing_unit = self.billing_unit

        pricing_model = self.pricing_model

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "credit_cost": credit_cost,
                "pricing_note": pricing_note,
            }
        )
        if billing_unit is not UNSET:
            field_dict["billing_unit"] = billing_unit
        if pricing_model is not UNSET:
            field_dict["pricing_model"] = pricing_model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credit_cost = d.pop("credit_cost")

        pricing_note = d.pop("pricing_note")

        billing_unit = cast(Literal["credits"] | Unset, d.pop("billing_unit", UNSET))
        if billing_unit != "credits" and not isinstance(billing_unit, Unset):
            raise ValueError(
                f"billing_unit must match const 'credits', got '{billing_unit}'"
            )

        pricing_model = cast(
            Literal["ubi_fixed_operation_credits_v1"] | Unset,
            d.pop("pricing_model", UNSET),
        )
        if pricing_model != "ubi_fixed_operation_credits_v1" and not isinstance(
            pricing_model, Unset
        ):
            raise ValueError(
                f"pricing_model must match const 'ubi_fixed_operation_credits_v1', got '{pricing_model}'"
            )

        fixed_credit_price_response = cls(
            credit_cost=credit_cost,
            pricing_note=pricing_note,
            billing_unit=billing_unit,
            pricing_model=pricing_model,
        )

        return fixed_credit_price_response
