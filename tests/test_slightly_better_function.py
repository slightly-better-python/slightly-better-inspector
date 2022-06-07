import unittest
from inspect import Parameter
from typing import TYPE_CHECKING
from typing import Union
from typing import Optional

from slightly_better_function import SlightlyBetterFunction

if TYPE_CHECKING:
    from typing import Generator


class TestSlightlyBetterFunction(unittest.TestCase):

    integer: int = 1
    string: str = 'string'

    def true_values(self) -> "Generator":
        # Arg test
        yield ['', [], {}]
        #
        yield ['a: int', [self.integer], {}]
        yield ['a: str', [self.string], {}]
        yield ['*args: str', [self.string, self.string], {}]
        #
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

    def false_values(self) -> "Generator":
        yield ['a: str', [self.integer], {}]

        # Too many values
        yield['a: str', [self.string, self.string], {}]

        # Too few values
        yield ['a: str, b: str', [self.string], {}]

        # wrong Args type
        yield ['*args: str', [self.integer, self.integer], {}]

    def test_true_values(self):
        for definition, args, kwargs in self.true_values():
            f = self._make_method(definition)
            assert f.accepts(*args, **kwargs)

    def test_false_values(self):
        for definition, args, kwargs in self.false_values():
            f = self._make_method(definition)
            assert not f.accepts(*args, *kwargs)

    def _make_method(self, definition: str) -> SlightlyBetterFunction:
        exec(f"class TestClass:\n\tdef test(self,{definition}):\n\t\tpass")
        return SlightlyBetterFunction(eval('TestClass.test'))




if __name__ == '__main__':
    unittest.main()
