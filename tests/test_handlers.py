import unittest
from typing import Dict

from slightly_better_types.handlers import Handlers


class Bar:

    def accepts_string(self, a: str):
        pass

    def accepts_string_too(self, b: str):
        pass

    def accepts_int(self, c: int):
        pass

    def _protected(self, a: Dict):
        pass

    def __private(self, a: Dict):
        pass

    @staticmethod
    def static(a: float):
        pass


class TestHandlers(unittest.TestCase):

    def test_find(self):
        handlers = Handlers(Bar)

        assert ['accepts_string', 'accepts_string_too'] == list(handlers.accepts('string').all().keys())
        assert ['accepts_string_too'] == list(handlers.accepts(b='string').all().keys())
        assert ['accepts_int'] == list(handlers.accepts(1).all().keys())

        class TestClass:
            pass

        assert [] == list(handlers.accepts(TestClass()).all().keys())

    def test_first(self):
        handlers = Handlers(Bar)
        assert 'accepts_string' == handlers.accepts('string').first().get_name()
        assert 'accepts_string_too' == handlers.accepts(b='string').first().get_name()

        class TestClass:
            pass

        assert None is handlers.accepts(TestClass()).first()

    def test_visibility(self):
        assert None is Handlers.new(Bar).public().accepts([]).first()
        assert None is Handlers.new(Bar).protected().accepts([]).first()
        assert Handlers.new(Bar).private().accepts({}).first() is not None
        assert Handlers.new(Bar).public().protected().accepts({}).first() is not None

    def test_all(self):
        assert 1 == len(Handlers.new(Bar).private().all())
        assert 4 == len(Handlers.new(Bar).public().all())
        assert 6 == len(Handlers.new(Bar).all())
        assert 1 == len(Handlers.new(Bar).filter(lambda x: x.is_static()).all())

    def test_filter(self):
        assert Handlers.new(Bar).filter(lambda x: not x.is_static()).accepts(2.1).first() is None
        assert Handlers.new(Bar).filter(lambda x: x.is_static()).accepts(1.2).first() is not None


if __name__ == '__main__':
    unittest.main()
