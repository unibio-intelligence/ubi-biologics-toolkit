from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UsagePlanLimitsResponse")


@_attrs_define
class UsagePlanLimitsResponse:
    """
    Attributes:
        active_gpu_jobs (int):
        active_jobs (int):
        chat_responses (int):
        cpu_scientific_jobs (int):
        gpu_scientific_jobs (int):
        monthly_scientific_credits (int):
        scientific_credits (int):
        window_seconds (int):
    """

    active_gpu_jobs: int
    active_jobs: int
    chat_responses: int
    cpu_scientific_jobs: int
    gpu_scientific_jobs: int
    monthly_scientific_credits: int
    scientific_credits: int
    window_seconds: int

    def to_dict(self) -> dict[str, Any]:
        active_gpu_jobs = self.active_gpu_jobs

        active_jobs = self.active_jobs

        chat_responses = self.chat_responses

        cpu_scientific_jobs = self.cpu_scientific_jobs

        gpu_scientific_jobs = self.gpu_scientific_jobs

        monthly_scientific_credits = self.monthly_scientific_credits

        scientific_credits = self.scientific_credits

        window_seconds = self.window_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "active_gpu_jobs": active_gpu_jobs,
                "active_jobs": active_jobs,
                "chat_responses": chat_responses,
                "cpu_scientific_jobs": cpu_scientific_jobs,
                "gpu_scientific_jobs": gpu_scientific_jobs,
                "monthly_scientific_credits": monthly_scientific_credits,
                "scientific_credits": scientific_credits,
                "window_seconds": window_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active_gpu_jobs = d.pop("active_gpu_jobs")

        active_jobs = d.pop("active_jobs")

        chat_responses = d.pop("chat_responses")

        cpu_scientific_jobs = d.pop("cpu_scientific_jobs")

        gpu_scientific_jobs = d.pop("gpu_scientific_jobs")

        monthly_scientific_credits = d.pop("monthly_scientific_credits")

        scientific_credits = d.pop("scientific_credits")

        window_seconds = d.pop("window_seconds")

        usage_plan_limits_response = cls(
            active_gpu_jobs=active_gpu_jobs,
            active_jobs=active_jobs,
            chat_responses=chat_responses,
            cpu_scientific_jobs=cpu_scientific_jobs,
            gpu_scientific_jobs=gpu_scientific_jobs,
            monthly_scientific_credits=monthly_scientific_credits,
            scientific_credits=scientific_credits,
            window_seconds=window_seconds,
        )

        return usage_plan_limits_response
