from inspect import Parameter
from inspect import signature
from types import FunctionType
from typing import Any
from typing import get_type_hints
from typing import List

from slightly_better_parameter import SlightlyBetterParameter
from utils import get_class_that_defined_method


class SlightlyBetterFunction:
    PUBLIC = 'public'
    PROTECTED = 'protected'
    PRIVATE = 'private'

    def __init__(self, _function):
        self._function = _function
        # self.positional_types = []
        # self.named_types = {}

        self.parameters = {
            Parameter.KEYWORD_ONLY: [],
            Parameter.VAR_KEYWORD: [],
            Parameter.VAR_POSITIONAL: [],
            Parameter.POSITIONAL_ONLY: [],
            Parameter.POSITIONAL_OR_KEYWORD: []
        }


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
                type_hint=type_hints.get(parameter.name),
            )
            for parameter in parameter_list
        ]

        for sb_parameter in sb_parameters:
            print(sb_parameter.name)
            print('first for loop?')
            # if sb_parameter.kind == Parameter.POSITIONAL_OR_KEYWORD:
            #     self.positional_or_keyword_types.append(sb_parameter)
            # elif sb_parameter.kind == Parameter.VAR_POSITIONAL
            self.parameters[sb_parameter.kind].append(sb_parameter)

            # self.positional_types.append(sb_parameter)
            # self.named_types[sb_parameter.name] = sb_parameter
            self.kinds.append(sb_parameter.kind)

        self.input_count = len(self.parameters.values())

    def accepts(self, *args: Any, **kwargs) -> bool:
        try:
            print([param.name for param in self.parameters[Parameter.POSITIONAL_OR_KEYWORD]])
            param_names = [param.name for param in self.parameters[Parameter.POSITIONAL_OR_KEYWORD]]
            if 'self' in param_names or 'cls' in param_names:
                args = [None, *args]
            self._signature.bind(*args, **kwargs)
        except TypeError:
            return False

        positionally_accepting_params: List[SlightlyBetterParameter] = [
            *self.parameters[Parameter.POSITIONAL_ONLY],
            *self.parameters[Parameter.POSITIONAL_OR_KEYWORD],
            *self.parameters[Parameter.VAR_POSITIONAL],
        ]

        for index, arg in enumerate(args):
            try:
                current_param = positionally_accepting_params[index]
                if not current_param.accepts(arg):
                    return False
            except IndexError:
                if (
                        positionally_accepting_params[-1].kind == Parameter.VAR_POSITIONAL
                        and positionally_accepting_params[-1].accepts(arg)
                ):
                    continue
                else:
                    return False

        kwarg_accepting_params = {}
        for param in [
            *self.parameters[Parameter.POSITIONAL_OR_KEYWORD],
            *self.parameters[Parameter.KEYWORD_ONLY],
            *self.parameters[Parameter.VAR_KEYWORD],
        ]:
            kwarg_accepting_params[param.name] = param

        for key, value in kwargs.items():
            if key not in kwarg_accepting_params:
                if (
                        self.parameters[Parameter.VAR_KEYWORD]
                        and not self.parameters[Parameter.VAR_KEYWORD][0].accepts(value)
                ):
                    return False
            elif not kwarg_accepting_params[key].accepts(value):
                return False
        return True

    def get_name(self) -> str:
        return self._function.__qualname__

    # def get_types(self) -> dict:
    #     return self.named_types

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
