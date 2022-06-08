from __future__ import annotations

from copy import copy
from inspect import isclass
from inspect import isfunction
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional

from slightly_better_types.function import Function


class Handlers:

    def __init__(self, _class):
        self._class = _class
        self.methods = {
            func_name: Function(
                getattr(self._class, func_name)
            ) for func_name in dir(self._class)
            if isfunction(getattr(self._class, func_name))
        }
        self.filters = []
        self.visibility_filters = []

    @staticmethod
    def new(class_or_class_instance: Any):
        if not isclass(class_or_class_instance):
            _class = type(class_or_class_instance)
        else:
            _class = class_or_class_instance
        return Handlers(_class)

    def accepts(self, *args, **kwargs) -> Handlers:
        func: Callable[[Function], bool] = lambda method: method.accepts(*args, **kwargs)
        return self.filter(func)

    def all(self) -> Dict[str, Function]:
        all_methods = {}
        for func_name, func in self.methods.items():
            if not self._filter_allows(method=func):
                continue

            all_methods[func_name] = func
        return all_methods

    def filter(self, _filter: Callable[..., bool]) -> Handlers:
        clone = copy(self)
        clone.filters = self.filters[:]
        clone.filters.append(_filter)
        return clone

    def first(self) -> Optional[Function]:
        return next(iter(self.all().values()), None)

    def public(self) -> Handlers:
        clone = copy(self)
        clone.visibility_filters = self.visibility_filters[:]
        clone.visibility_filters = Function.PUBLIC
        return clone

    def protected(self) -> Handlers:
        clone = copy(self)
        clone.visibility_filters = self.visibility_filters[:]
        clone.visibility_filters = Function.PROTECTED
        return clone

    def private(self) -> Handlers:
        clone = copy(self)
        clone.visibility_filters = self.visibility_filters[:]
        clone.visibility_filters = Function.PRIVATE
        return clone

    def _filter_allows(self, method: Function) -> bool:
        if self.visibility_filters and method.visibility() not in self.visibility_filters:
            return False

        for _filter in self.filters:
            if _filter(method) is False:
                return False

        return True
