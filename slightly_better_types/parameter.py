from __future__ import annotations

from inspect import Parameter as InspectParameter
from typing import Any

from izzet import izzet


class Parameter(InspectParameter):

    def __init__(self, type_hint, *args, **kwargs):
        super(Parameter, self).__init__(*args, **kwargs)
        self.accepted_type = type_hint

    @staticmethod
    def new(parameter: InspectParameter, type_hint: str) -> Parameter:
        return Parameter(
            name=parameter.name,
            kind=parameter.kind,
            default=parameter.default,
            annotation=parameter.annotation,
            type_hint=type_hint,
        )

    def get_name(self) -> str:
        return self.name

    def accepts(self, _input: Any) -> bool:
        return izzet(_input).a(self.accepted_type)
