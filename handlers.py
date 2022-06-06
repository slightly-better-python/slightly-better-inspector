from inspect import isfunction
from inspect import Parameter
from inspect import signature
from typing import Any
from typing import get_args
from typing import get_origin
from typing import get_type_hints
from typing import Optional
from typing import Union
from types import FunctionType

from utils import get_class_that_defined_method


class Handlers:
    def __init__(self, _class):
        self._class = _class
        self.methods = [func for func in dir(_class) if isfunction(getattr(_class, func)) and '__' not in func]








def accepts(
        test,
        int_arg: int,
        str_arg: str = "mr sister",
        str_arg_default: Optional[str] = None,
        *args: Any,
        **kwargs
) -> bool:
    return False


if __name__ == "__main__":
    f = Function(accepts)
    # print(accepts.__qualname__)
    print(f.get_name())
    print(f.get_types())
    # r = f.accepts(1, 2, 'three', None, 1, 2, 3, 4, 5, tesat='positional', another_one='asdasd')
    # print(r)
