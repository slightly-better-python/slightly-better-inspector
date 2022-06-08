# slightly-better-types

... arguably

Improved abstraction for dealing with union and named types.

## Installation

```bash
pip install slightly-better-types==0.0.1
```

## Usage

Using the `Function` class:

```python
from slightly_better_types.function import Function


def accepts_string(a: str, b: int):
    pass


sb_function = Function(accepts_string)

sb_function.accepts('string', 1)  # True
sb_function.accepts(1, 'string')  # False
sb_function.accepts('string')  # False
```

Using `Handlers` to determine which methods accept a given set of input:

```python
from slightly_better_types.handlers import Handlers


class Bar:
    def accepts_string(self, a: str):
        pass

    def accepts_string_too(self, a: str):
        pass

    def accepts_int(self, a: int):
        pass


handlers = Handlers(Bar)
list(handlers.accepts('a string').all().keys())  # ['accepts_string', 'accepts_string_too']
list(handlers.accepts(1).first().get_name())  # 'accepts_int'
```

## Tests

```bash
python3 -m unittest
```

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
