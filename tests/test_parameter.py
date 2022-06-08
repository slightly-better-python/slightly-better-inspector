import unittest
import inspect
from abc import ABC
from typing import Any # noqa
from types import FunctionType
from typing import Dict
from typing import Union # noqa
from typing import get_type_hints
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from slightly_better_types.parameter import Parameter

if TYPE_CHECKING:
    from typing import Generator


class AbstractFoo(ABC):
    pass


class Foo(AbstractFoo):
    def __init__(self):
        pass


class TestSlightlyBetterParameter(unittest.TestCase):

    boolean: bool = True
    integer: int = 1
    _float: float = 1.2
    string: str = 'string'
    _list: List = []
    _dict: Dict = {}
    _none = None
    foo: Foo

    def true_values(self) -> "Generator":

        self.foo = Foo()

        yield ['a: Any', self.boolean]
        yield ['a: bool', self.boolean]
        yield ['a: Union[int, bool]', self.boolean]

        yield ['a: Any', self._float]
        yield ['a: float', self._float]
        yield ['a: Union[int, float]', self._float]

        yield ['a: Any', self.integer]
        yield ['a: int', self.integer]
        yield ['a: Union[int, str]', self.integer]

        yield ['a: Any', self.string]
        yield ['a: str', self.string]
        yield ['a: Union[int, str]', self.string]

        yield ['a: Any', [self.string]]
        yield ['a: List[str]', [self.string]]
        yield ['a: Union[int, List[str]]', [self.string]]

        yield ['a: Any', self._none]
        yield ['a: Optional[str]', self._none]
        yield ['a: Union[int, Optional[str]]', self._none]

        yield ['a: Any', self.foo]
        yield ['a: Optional[Foo]', self.foo]
        yield ['a: AbstractFoo', self.foo]

    def false_values(self):
        yield ['a: Union[str, int]', []]
        yield ['a: Union[str, int]', None]
        yield ['a: int', 'invalid']
        yield ['a: int', 2.1]

    def test_true(self):
        for definition, arg in self.true_values():
            assert self._make_type(definition).accepts(arg)

    def test_false(self):
        for definition, arg in self.false_values():
            assert not self._make_type(definition).accepts(arg)

    def _make_type(self, definition: str) -> Optional[Parameter]:
        exec(f"class TestClass:\n\tdef test(self,{definition}):\n\t\tpass")
        func: FunctionType = (eval('TestClass.test'))
        param = list(inspect.signature(func).parameters.values())[1]
        if param:
            type_hints = get_type_hints(func)
            return Parameter(
                name=param.name,
                kind=param.kind,
                default=param.default,
                annotation=param.annotation,
                type_hint=type_hints.get(param.name)
            )
        return None
