import unittest


class Bar:

    def accepts_string(self, a: str):
        pass

    def accepts_string_too(self, b: str):
        pass

    def accepts_int(self, c: int):
        pass

    def __invisible__(self, *args):
        pass


class TestHandlers(unittest.TestCase):
    pass
