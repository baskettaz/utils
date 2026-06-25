import bisect
import re
import sys
from collections import deque
from collections import OrderedDict
from copy import deepcopy
from numbers import Number
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Iterable
from typing import overload
from typing import SupportsIndex



class DefaultDictMixin(dict):
    "Custom ordered dictionary, similar to the classic defaultdict"

    # Source: http://stackoverflow.com/a/6190500/562769

    def __init__(self, default_factory: Callable | None = None, /, *a, **kw):
        if default_factory is not None and not callable(default_factory):
            raise TypeError("first argument must be callable")
        super().__init__(*a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key) -> Any:
        try:
            return super().__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key) -> Any:
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self) -> tuple:
        args = tuple() if self.default_factory is None else (self.default_factory,)
        return type(self), args, None, None, iter(self.items())

    def copy(self) -> Self:
        return self.__copy__()

    def __copy__(self) -> Self:
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo) -> Self:
        return type(self)(self.default_factory, deepcopy(dict(self)))

    def __repr__(self) -> str:
        default = f"{self.default_factory}"
        text = f"{super().__repr__()}"
        indx = text.index("(") + 1
        return "".join([text[:indx], default, ", ", text[indx:]])


class DefaultOrderedDict(DefaultDictMixin, OrderedDict):
    pass
