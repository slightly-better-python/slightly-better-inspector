from __future__ import annotations

from copy import copy
from inspect import isclass
from inspect import isfunction
from typing import Any
from typing import Callable
from typing import List
from typing import Optional

from slightly_better_function import SlightlyBetterFunction


class Handlers:

    def __init__(self, _class):
        self._class = _class
        self.methods = {
            func_name: SlightlyBetterFunction(
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
        func: Callable[[SlightlyBetterFunction], bool] = lambda method: method.accepts(*args, **kwargs)
        return self.filter(func)

    def all(self) -> List[SlightlyBetterFunction]:
        all_methods = []
        for func_name, func in self.methods.items():
            if not self._filter_allows(method=func):
                continue

            all_methods.append(func)
        return all_methods

    def filter(self, _filter: Callable[..., bool]) -> Handlers:
        clone = copy(self)
        clone.filters = self.filters[:]
        clone.filters.append(_filter)
        return clone

    def first(self) -> Optional[SlightlyBetterFunction]:
        return next(iter(self.all()), None)

    def public(self) -> Handlers:
        clone = copy(self)
        clone.visibility_filters = self.visibility_filters[:]
        clone.visibility_filters = SlightlyBetterFunction.PUBLIC
        return clone

    def protected(self) -> Handlers:
        clone = copy(self)
        clone.visibility_filters = self.visibility_filters[:]
        clone.visibility_filters = SlightlyBetterFunction.PROTECTED
        return clone

    def private(self) -> Handlers:
        clone = copy(self)
        clone.visibility_filters = self.visibility_filters[:]
        clone.visibility_filters = SlightlyBetterFunction.PRIVATE
        return clone

    def _filter_allows(self, method: SlightlyBetterFunction) -> bool:
        print(method.visibility())
        print(self.visibility_filters)
        if self.visibility_filters and method.visibility() not in self.visibility_filters:
            print('returning false')
            return False
        else:
            print('is true')

        for _filter in self.filters:
            if _filter(method) is False:
                return False

        return True
