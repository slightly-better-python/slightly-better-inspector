import unittest
from typing import List

from handlers import Handlers


class Bar:

    def accepts_string(self, a: str):
        pass

    def accepts_string_too(self, b: str):
        pass

    def accepts_int(self, c: int):
        pass

    def _protected(self, _list: List[str]):
        pass

    def __private(self, a: str):
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
        assert Handlers.new(Bar).private().accepts(['string']).first() is not None


#         $this->assertNotNull(Handlers::new(Baz::class)->private()->accepts([])->first());
#         $this->assertNotNull(Handlers::new(Baz::class)->public()->protected()->private()->accepts([])->first());
#     }

if __name__ == '__main__':
    unittest.main()
