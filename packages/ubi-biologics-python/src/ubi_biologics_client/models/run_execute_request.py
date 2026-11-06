from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.run_mode import RunMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.input_binding import InputBinding
    from ..models.run_execute_request_parameters import RunExecuteRequestParameters


T = TypeVar("T", bound="RunExecuteRequest")


@_attrs_define
class RunExecuteRequest:
    """
    Attributes:
        capability_id (str):
        destination_project_id (str):
        expected_preview_digest (str):
        agent_run_id (None | str | Unset):
        capability_version (None | str | Unset):
        inputs (list[InputBinding] | Unset):
        mode (RunMode | Unset):
        parameters (RunExecuteRequestParameters | Unset):
        preview_receipt (None | str | Unset):
    """

    capability_id: str
    destination_project_id: str
    expected_preview_digest: str
    agent_run_id: None | str | Unset = UNSET
    capability_version: None | str | Unset = UNSET
    inputs: list[InputBinding] | Unset = UNSET
    mode: RunMode | Unset = UNSET
    parameters: RunExecuteRequestParameters | Unset = UNSET
    preview_receipt: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        capability_id = self.capability_id

        destination_project_id = self.destination_project_id

        expected_preview_digest = self.expected_preview_digest

        agent_run_id: None | str | Unset
        if isinstance(self.agent_run_id, Unset):
            agent_run_id = UNSET
        else:
            agent_run_id = self.agent_run_id

        capability_version: None | str | Unset
        if isinstance(self.capability_version, Unset):
            capability_version = UNSET
        else:
            capability_version = self.capability_version

        inputs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.inputs, Unset):
            inputs = []
            for inputs_item_data in self.inputs:
                inputs_item = inputs_item_data.to_dict()
                inputs.append(inputs_item)

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        parameters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        preview_receipt: None | str | Unset
        if isinstance(self.preview_receipt, Unset):
            preview_receipt = UNSET
        else:
            preview_receipt = self.preview_receipt

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "capability_id": capability_id,
                "destination_project_id": destination_project_id,
                "expected_preview_digest": expected_preview_digest,
            }
        )
        if agent_run_id is not UNSET:
            field_dict["agent_run_id"] = agent_run_id
        if capability_version is not UNSET:
            field_dict["capability_version"] = capability_version
        if inputs is not UNSET:
            field_dict["inputs"] = inputs
        if mode is not UNSET:
            field_dict["mode"] = mode
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if preview_receipt is not UNSET:
            field_dict["preview_receipt"] = preview_receipt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.input_binding import InputBinding
        from ..models.run_execute_request_parameters import RunExecuteRequestParameters

        d = dict(src_dict)
        capability_id = d.pop("capability_id")

        destination_project_id = d.pop("destination_project_id")

        expected_preview_digest = d.pop("expected_preview_digest")

        def _parse_agent_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_run_id = _parse_agent_run_id(d.pop("agent_run_id", UNSET))

        def _parse_capability_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        capability_version = _parse_capability_version(
            d.pop("capability_version", UNSET)
        )

        _inputs = d.pop("inputs", UNSET)
        inputs: list[InputBinding] | Unset = UNSET
        if _inputs is not UNSET:
            inputs = []
            for inputs_item_data in _inputs:
                inputs_item = InputBinding.from_dict(inputs_item_data)

                inputs.append(inputs_item)

        _mode = d.pop("mode", UNSET)
        mode: RunMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = RunMode(_mode)

        _parameters = d.pop("parameters", UNSET)
        parameters: RunExecuteRequestParameters | Unset
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = RunExecuteRequestParameters.from_dict(_parameters)

        def _parse_preview_receipt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        preview_receipt = _parse_preview_receipt(d.pop("preview_receipt", UNSET))

        run_execute_request = cls(
            capability_id=capability_id,
            destination_project_id=destination_project_id,
            expected_preview_digest=expected_preview_digest,
            agent_run_id=agent_run_id,
            capability_version=capability_version,
            inputs=inputs,
            mode=mode,
            parameters=parameters,
            preview_receipt=preview_receipt,
        )

        return run_execute_request
