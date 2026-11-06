from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.run_mode import RunMode
from ..models.run_state import RunState
from ..models.side_effect_class import SideEffectClass
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_response_failure_type_0 import RunResponseFailureType0
    from ..models.run_response_input_snapshot import RunResponseInputSnapshot
    from ..models.run_response_output_manifest_item import RunResponseOutputManifestItem
    from ..models.run_response_parameters import RunResponseParameters


T = TypeVar("T", bound="RunResponse")


@_attrs_define
class RunResponse:
    """
    Attributes:
        binding_digest (str):
        capability_id (str):
        capability_version (str):
        created_at (str):
        destination_project_id (str):
        id (str):
        initiating_principal_id (str):
        input_snapshot (RunResponseInputSnapshot):
        mode (RunMode):
        output_manifest (list[RunResponseOutputManifestItem]):
        parameters (RunResponseParameters):
        side_effect_class (SideEffectClass):
        state (RunState):
        updated_at (str):
        agent_run_id (None | str | Unset):
        completed_at (None | str | Unset):
        failure (None | RunResponseFailureType0 | Unset):
        parent_run_id (None | str | Unset):
    """

    binding_digest: str
    capability_id: str
    capability_version: str
    created_at: str
    destination_project_id: str
    id: str
    initiating_principal_id: str
    input_snapshot: RunResponseInputSnapshot
    mode: RunMode
    output_manifest: list[RunResponseOutputManifestItem]
    parameters: RunResponseParameters
    side_effect_class: SideEffectClass
    state: RunState
    updated_at: str
    agent_run_id: None | str | Unset = UNSET
    completed_at: None | str | Unset = UNSET
    failure: None | RunResponseFailureType0 | Unset = UNSET
    parent_run_id: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.run_response_failure_type_0 import RunResponseFailureType0

        binding_digest = self.binding_digest

        capability_id = self.capability_id

        capability_version = self.capability_version

        created_at = self.created_at

        destination_project_id = self.destination_project_id

        id = self.id

        initiating_principal_id = self.initiating_principal_id

        input_snapshot = self.input_snapshot.to_dict()

        mode = self.mode.value

        output_manifest = []
        for output_manifest_item_data in self.output_manifest:
            output_manifest_item = output_manifest_item_data.to_dict()
            output_manifest.append(output_manifest_item)

        parameters = self.parameters.to_dict()

        side_effect_class = self.side_effect_class.value

        state = self.state.value

        updated_at = self.updated_at

        agent_run_id: None | str | Unset
        if isinstance(self.agent_run_id, Unset):
            agent_run_id = UNSET
        else:
            agent_run_id = self.agent_run_id

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = self.completed_at

        failure: dict[str, Any] | None | Unset
        if isinstance(self.failure, Unset):
            failure = UNSET
        elif isinstance(self.failure, RunResponseFailureType0):
            failure = self.failure.to_dict()
        else:
            failure = self.failure

        parent_run_id: None | str | Unset
        if isinstance(self.parent_run_id, Unset):
            parent_run_id = UNSET
        else:
            parent_run_id = self.parent_run_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "binding_digest": binding_digest,
                "capability_id": capability_id,
                "capability_version": capability_version,
                "created_at": created_at,
                "destination_project_id": destination_project_id,
                "id": id,
                "initiating_principal_id": initiating_principal_id,
                "input_snapshot": input_snapshot,
                "mode": mode,
                "output_manifest": output_manifest,
                "parameters": parameters,
                "side_effect_class": side_effect_class,
                "state": state,
                "updated_at": updated_at,
            }
        )
        if agent_run_id is not UNSET:
            field_dict["agent_run_id"] = agent_run_id
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if failure is not UNSET:
            field_dict["failure"] = failure
        if parent_run_id is not UNSET:
            field_dict["parent_run_id"] = parent_run_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_response_failure_type_0 import RunResponseFailureType0
        from ..models.run_response_input_snapshot import RunResponseInputSnapshot
        from ..models.run_response_output_manifest_item import (
            RunResponseOutputManifestItem,
        )
        from ..models.run_response_parameters import RunResponseParameters

        d = dict(src_dict)
        binding_digest = d.pop("binding_digest")

        capability_id = d.pop("capability_id")

        capability_version = d.pop("capability_version")

        created_at = d.pop("created_at")

        destination_project_id = d.pop("destination_project_id")

        id = d.pop("id")

        initiating_principal_id = d.pop("initiating_principal_id")

        input_snapshot = RunResponseInputSnapshot.from_dict(d.pop("input_snapshot"))

        mode = RunMode(d.pop("mode"))

        output_manifest = []
        _output_manifest = d.pop("output_manifest")
        for output_manifest_item_data in _output_manifest:
            output_manifest_item = RunResponseOutputManifestItem.from_dict(
                output_manifest_item_data
            )

            output_manifest.append(output_manifest_item)

        parameters = RunResponseParameters.from_dict(d.pop("parameters"))

        side_effect_class = SideEffectClass(d.pop("side_effect_class"))

        state = RunState(d.pop("state"))

        updated_at = d.pop("updated_at")

        def _parse_agent_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_run_id = _parse_agent_run_id(d.pop("agent_run_id", UNSET))

        def _parse_completed_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        def _parse_failure(data: object) -> None | RunResponseFailureType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                failure_type_0 = RunResponseFailureType0.from_dict(data)

                return failure_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunResponseFailureType0 | Unset, data)

        failure = _parse_failure(d.pop("failure", UNSET))

        def _parse_parent_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_run_id = _parse_parent_run_id(d.pop("parent_run_id", UNSET))

        run_response = cls(
            binding_digest=binding_digest,
            capability_id=capability_id,
            capability_version=capability_version,
            created_at=created_at,
            destination_project_id=destination_project_id,
            id=id,
            initiating_principal_id=initiating_principal_id,
            input_snapshot=input_snapshot,
            mode=mode,
            output_manifest=output_manifest,
            parameters=parameters,
            side_effect_class=side_effect_class,
            state=state,
            updated_at=updated_at,
            agent_run_id=agent_run_id,
            completed_at=completed_at,
            failure=failure,
            parent_run_id=parent_run_id,
        )

        return run_response
