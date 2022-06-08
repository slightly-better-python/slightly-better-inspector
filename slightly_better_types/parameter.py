from inspect import isclass
from inspect import Parameter as InspectParameter
from typing import Any
from typing import get_args
from typing import get_origin
from typing import Optional
from typing import Union


class Parameter(InspectParameter):
    TYPE_MAPPING = {
        int: 'integer',
        bool: 'boolean',
        float: 'float',
        str: 'string',
        tuple: 'tuple'
    }

    def __init__(self, type_hint, *args, **kwargs):
        super(Parameter, self).__init__(*args, **kwargs)
        self.type_hint = type_hint
        self.is_noneable = self.default != self.empty
        self.is_annotated = self.annotation != self.empty
        self.is_any = False
        self.type_name = ''
        self.accepted_types = []

        if not self.is_annotated:
            self.accepted_types.append(Any)
            self.is_any = True
        else:
            is_union_type = get_origin(self.annotation) == Union
            if not is_union_type:
                self.accepted_types = [self.type_hint]
                self.is_any = self.annotation == Any
                self.type_name = self.TYPE_MAPPING.get(self.type_hint, str(self.type_hint))
            else:
                self.accepted_types = list(get_args(self.type_hint))

                names = []
                for accepted_type in self.accepted_types:
                    if accepted_type == Any:
                        self.is_any = True
                    names.append(
                        self.TYPE_MAPPING.get(accepted_type, str(accepted_type))
                    )

                self.type_name = '|'.join(names)

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
