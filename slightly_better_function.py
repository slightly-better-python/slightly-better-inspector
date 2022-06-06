from inspect import Parameter
from inspect import signature
from types import FunctionType
from typing import Any
from typing import get_type_hints

from slightly_better_parameter import SlightlyBetterParameter
from utils import get_class_that_defined_method


class SlightlyBetterFunction:
    PUBLIC = 'public'
    PROTECTED = 'protected'
    PRIVATE = 'private'

    def __init__(self, _function):
        self._function = _function
        self.positional_types = []
        self.named_types = {}

        # signature returns whatever is in the function's __annotation__ attribute
        # which could get distorted if `__future__.annotations` is used anywhere
        self._signature = signature(self._function)

        type_hints = get_type_hints(self._function)
        parameter_list = list(self._signature.parameters.values())
        self.kinds = []

        sb_parameters = [
            SlightlyBetterParameter(
                name=parameter.name,
                kind=parameter.kind,
                default=parameter.default,
                annotation=parameter.annotation,
                type_hint=type_hints.get(parameter.name)
            )
            for parameter in parameter_list if parameter.name not in ['self', 'cls']
        ]
        for sb_parameter in sb_parameters:
            self.positional_types.append(sb_parameter)
            self.named_types[sb_parameter.name] = sb_parameter
            self.kinds.append(sb_parameter.kind)

        self.input_count = len(self.positional_types)

    def accepts(self, *args: Any, **kwargs) -> bool:
        parameter_types = self.positional_types

        if (
                Parameter.VAR_KEYWORD not in self.kinds
                and Parameter.VAR_POSITIONAL not in self.kinds
                and len(args) + len(kwargs) < self.input_count - 2
        ):
            return False

        for index, parameter_type in enumerate(parameter_types):
            try:
                current_arg = args[index]
            except IndexError:
                if parameter_type.kind in [Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL]:
                    return True
                return False

            if not parameter_type.accepts(current_arg):
                return False

        return True

    def get_name(self) -> str:
        return self._function.__qualname__

    def get_types(self) -> dict:
        return self.named_types

    def visibility(self) -> str:
        name = self.get_name()
        if name.startswith('__'):
            return self.PRIVATE
        elif name.startswith('_'):
            return self.PROTECTED
        else:
            return self.PUBLIC

    def is_static(self):
        _class = get_class_that_defined_method(self._function)
        return _class is not None and isinstance(self._function, FunctionType)

    def is_abstract(self):
        return hasattr(self._function, '__isabstractmethod__')

    def is_public(self):
        return not self.get_name().startswith('_')

    def is_protected(self):
        return self.get_name().startswith('_') and not self.get_name().startswith('__')

    def is_private(self):
        return self.get_name().startswith('__')
