# slightly-better-types

... arguably

Improved abstraction for dealing with union and named types.

## Installation

```bash
pip install slightly-better-types==1.0.0
```

## Usage

Using the `Parameter` class directly

```python
from inspect import signature
from typing import get_type_hints
from slightly_better_types.parameter import Parameter


class Foo:
    pass


def accepts_string(a: Foo):
    pass


signature = signature(accepts_string)
type_hints = get_type_hints(get_type_hints(accepts_string))

parameter = list((signature.parameters.values()))[0]
parameter = Parameter(parameter=parameter, type_hint=type_hints.get(parameter.name))

parameter.accepts(1)  # False
parameter.accepts(Foo())  # True


```

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
