from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_predicate import FilterPredicate


T = TypeVar("T", bound="FilterExpression")


@_attrs_define
class FilterExpression:
    """
    Attributes:
        combinator (str | Unset):  Default: 'and'.
        expressions (list[FilterExpression] | Unset):
        predicates (list[FilterPredicate] | Unset):
    """

    combinator: str | Unset = "and"
    expressions: list[FilterExpression] | Unset = UNSET
    predicates: list[FilterPredicate] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        combinator = self.combinator

        expressions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.expressions, Unset):
            expressions = []
            for expressions_item_data in self.expressions:
                expressions_item = expressions_item_data.to_dict()
                expressions.append(expressions_item)

        predicates: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.predicates, Unset):
            predicates = []
            for predicates_item_data in self.predicates:
                predicates_item = predicates_item_data.to_dict()
                predicates.append(predicates_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if combinator is not UNSET:
            field_dict["combinator"] = combinator
        if expressions is not UNSET:
            field_dict["expressions"] = expressions
        if predicates is not UNSET:
            field_dict["predicates"] = predicates

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_predicate import FilterPredicate

        d = dict(src_dict)
        combinator = d.pop("combinator", UNSET)

        _expressions = d.pop("expressions", UNSET)
        expressions: list[FilterExpression] | Unset = UNSET
        if _expressions is not UNSET:
            expressions = []
            for expressions_item_data in _expressions:
                expressions_item = FilterExpression.from_dict(expressions_item_data)

                expressions.append(expressions_item)

        _predicates = d.pop("predicates", UNSET)
        predicates: list[FilterPredicate] | Unset = UNSET
        if _predicates is not UNSET:
            predicates = []
            for predicates_item_data in _predicates:
                predicates_item = FilterPredicate.from_dict(predicates_item_data)

                predicates.append(predicates_item)

        filter_expression = cls(
            combinator=combinator,
            expressions=expressions,
            predicates=predicates,
        )

        return filter_expression
