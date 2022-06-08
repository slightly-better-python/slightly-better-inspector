from inspect import Parameter as InspectParameter
from inspect import signature
from typing import Any
from typing import get_type_hints
from typing import List

from slightly_better_types.parameter import Parameter
from slightly_better_types.utils import inspect_type


class Function:
    PUBLIC = 'public'
    PROTECTED = 'protected'
    PRIVATE = 'private'

    def __init__(self, _function):
        self._function = _function

        self.parameters = {
            InspectParameter.KEYWORD_ONLY: [],
            InspectParameter.VAR_KEYWORD: [],
            InspectParameter.VAR_POSITIONAL: [],
            InspectParameter.POSITIONAL_ONLY: [],
            InspectParameter.POSITIONAL_OR_KEYWORD: []
        }

        # signature returns whatever is in the function's __annotation__ attribute
        # which could get distorted if `__future__.annotations` is used anywhere
        self._signature = signature(self._function)

        type_hints = get_type_hints(self._function)
        parameter_list = list(self._signature.parameters.values())
        self.kinds = []

        sb_parameters = [
            Parameter(
                name=parameter.name,
                kind=parameter.kind,
                default=parameter.default,
                annotation=parameter.annotation,
                type_hint=type_hints.get(parameter.name),
            )
            for parameter in parameter_list
        ]

        for sb_parameter in sb_parameters:
            self.parameters[sb_parameter.kind].append(sb_parameter)
            self.kinds.append(sb_parameter.kind)

        self.input_count = len(self.parameters.values())

    def accepts(self, *args: Any, **kwargs) -> bool:
        try:
            param_names = [param.name for param in self.parameters[InspectParameter.POSITIONAL_OR_KEYWORD]]
            if 'self' in param_names or 'cls' in param_names:
                args = [None, *args]
            self._signature.bind(*args, **kwargs)
        except TypeError:
            return False

        positionally_accepting_params: List[Parameter] = [
            *self.parameters[InspectParameter.POSITIONAL_ONLY],
            *self.parameters[InspectParameter.POSITIONAL_OR_KEYWORD],
            *self.parameters[InspectParameter.VAR_POSITIONAL],
        ]

        for index, arg in enumerate(args):
            try:
                current_param = positionally_accepting_params[index]
                if not current_param.accepts(arg):
                    return False
            except IndexError:
                if (
                        positionally_accepting_params[-1].kind == InspectParameter.VAR_POSITIONAL
                        and positionally_accepting_params[-1].accepts(arg)
                ):
                    continue
                else:
                    return False

        kwarg_accepting_params = {}
        for param in [
            *self.parameters[InspectParameter.POSITIONAL_OR_KEYWORD],
            *self.parameters[InspectParameter.KEYWORD_ONLY],
            *self.parameters[InspectParameter.VAR_KEYWORD],
        ]:
            kwarg_accepting_params[param.name] = param

        for key, value in kwargs.items():
            if key not in kwarg_accepting_params:
                if (
                        self.parameters[InspectParameter.VAR_KEYWORD]
                        and not self.parameters[InspectParameter.VAR_KEYWORD][0].accepts(value)
                ):
                    return False
            elif not kwarg_accepting_params[key].accepts(value):
                return False
        return True

    def get_name(self) -> str:
        return self._function.__name__

    def visibility(self) -> str:
        name = self.get_name()
        if name.startswith('__'):
            return self.PRIVATE
        elif name.startswith('_'):
            return self.PROTECTED
        else:
            return self.PUBLIC

    def is_static(self):
        return inspect_type(self._function) == 'staticmethod'

    def is_abstract(self):
        return hasattr(self._function, '__isabstractmethod__')

    def is_public(self):
        return not self.get_name().startswith('_')

    def is_protected(self):
        return self.get_name().startswith('_') and not self.get_name().startswith('__')

    def is_private(self):
        return self.get_name().startswith('__')
