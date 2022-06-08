from __future__ import annotations

from inspect import isclass
from inspect import Parameter as InspectParameter
from typing import Any
from typing import get_args
from typing import Optional


class Parameter(InspectParameter):

    def __init__(self, type_hint, *args, **kwargs):
        super(Parameter, self).__init__(*args, **kwargs)
        self.type_hint = type_hint
        self.is_noneable = self.default != self.empty
        self.is_annotated = self.annotation != self.empty
        self.is_any = False
        self.accepted_types = []

        if not self.is_annotated:
            self.accepted_types.append(Any)
            self.is_any = True
        else:
            self.accepted_types = self.__get_accepted_types(self.type_hint)
            for accepted_type in self.accepted_types:
                if accepted_type == Any:
                    self.is_any = True

    @staticmethod
    def new(parameter: InspectParameter, type_hint: str) -> Parameter:
        return Parameter(
            name=parameter.name,
            kind=parameter.kind,
            default=parameter.default,
            annotation=parameter.annotation,
            type_hint=type_hint,
        )

    def __get_accepted_types(self, type_hint):
        results = []
        args = list(get_args(type_hint))
        if not args:
            return [type_hint]

        for arg in args:
            for r in self.__get_accepted_types(arg):
                results.append(r)

        return results

    def get_name(self) -> str:
        return self.name

    def accepts(self, _input: Any, key: Optional[str] = None) -> bool:
        if key and self.name != key:
            return False

        if self.is_any:
            return True

        if self.is_noneable and _input is None:
            return True

        if type(_input) in self.accepted_types:
            return True

        if isinstance(_input, list):
            results = []
            for item in _input:
                results.append(self.accepts(item))
            return all(results) and len(results) > 0

        extends_or_is = False
        for accepted_type in self.accepted_types:
            if not isclass(_input):
                input_class = type(_input)
            else:
                input_class = _input
            try:
                if issubclass(input_class, accepted_type):
                    extends_or_is = True
            except TypeError:
                continue

        if extends_or_is:
            return True

        return False
