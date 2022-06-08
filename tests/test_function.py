import unittest
from abc import ABC
from typing import Optional  # noqa
from typing import TYPE_CHECKING
from typing import Union  # noqa

from slightly_better_types.function import Function

if TYPE_CHECKING:
    from typing import Generator


class AbstractBar(ABC):
    pass


class Bar(AbstractBar):
    pass


class Foo:
    pass


class TestSlightlyBetterFunction(unittest.TestCase):
    integer: int = 1
    string: str = 'string'
    bar: Bar
    foo: Foo

    def true_values(self) -> "Generator":
        self.bar = Bar()

        # Arg test
        yield ['', [], {}]

        yield ['a: int', [self.integer], {}]
        yield ['a: str', [self.string], {}]
        yield ['*args: str', [self.string, self.string], {}]

        yield ['a: int, b: Union[int, str]', [self.integer, self.integer], {}]
        yield ['a: int, b: Union[int, str]', [self.integer, self.string], {}]

        yield ['a: Optional[int], b: Optional[int]', [None, None], {}]
        yield ['a: Optional[int], b: Optional[str]', [None, self.string], {}]

        # Kwarg Test
        yield [
            'a: int, b: Union[int, str], c: int = 2, *args, keyword_only: str, **kwargs',
            [],
            {'a': self.integer, 'b': self.string, 'keyword_only': 'word'}
        ]
        yield [
            'a: int, b: Union[int, str], c: int = 2, *args, keyword_only: str, **kwargs: str',
            [],
            {'a': self.integer, 'b': self.string, 'keyword_only': self.string, 'another_kwarg': self.string}
        ]

        # Inheritance
        yield ['bar: Bar, bar_2: AbstractBar', [self.bar, self.bar], {}]

    def false_values(self) -> "Generator":
        self.foo = Foo()

        yield ['a: str', [self.integer], {}]

        # Too many values
        yield ['', [self.string], {}]
        yield ['a: str', [self.string, self.string], {}]

        # Too few values
        yield ['a: str, b: str', [self.string], {}]

        # Wrong Args type
        yield ['*args: str', [self.integer, self.integer], {}]

        # Wrong kwargs type
        yield ['**args: str', [], {'keyword_arg': self.integer}]

        # Inheritance
        yield ['bar: Bar', [self.foo], {}]

    def test_true_values(self):
        for definition, args, kwargs in self.true_values():
            f = self._make_method(definition)
            assert f.accepts(*args, **kwargs)

    def test_false_values(self):
        for definition, args, kwargs in self.false_values():
            f = self._make_method(definition)
            assert not f.accepts(*args, *kwargs)

    def _make_method(self, definition: str) -> Function:
        exec(f"class TestClass:\n\tdef test(self,{definition}):\n\t\tpass")
        return Function(eval('TestClass.test'))


if __name__ == '__main__':
    unittest.main()
