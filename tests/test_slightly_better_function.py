import unittest
from typing import TYPE_CHECKING

from slightly_better_function import SlightlyBetterFunction

if TYPE_CHECKING:
    from typing import Generator


class TestSlightlyBetterFunction(unittest.TestCase):

    integer: int = 1
    string: str = 'string'

    def true_values(self) -> "Generator":
        yield ['', None]
        yield ['a: int', self.integer]
        yield ['a: str', self.string]

    def false_values(self) -> "Generator":
        yield ['a: str', self.integer]

    def test_true_values(self):
        for definition, args in self.true_values():
            f = self._make_method(definition)
            assert f.accepts(args)

    def test_false_values(self):
        for definition, args in self.false_values():
            f = self._make_method(definition)
            assert not f.accepts(args)

    def _make_method(self, definition: str) -> SlightlyBetterFunction:
        exec(f"class TestClass:\n\tdef test(self,{definition}):\n\t\tpass")
        return SlightlyBetterFunction(eval('TestClass.test'))




if __name__ == '__main__':
    unittest.main()
