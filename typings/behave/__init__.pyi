from __future__ import annotations

from typing import Callable

from typing_extensions import Concatenate, ParamSpec, TypeAlias

from .runner import Context

_P = ParamSpec("_P")

_ArgsStep: TypeAlias = Callable[Concatenate[Context, _P], None]
_NoArgsStep: TypeAlias = Callable[[Context], None]

_Step: TypeAlias = _NoArgsStep | _ArgsStep[str]

def given(phrase: str) -> Callable[[_Step], _Step]: ...
def when(phrase: str) -> Callable[[_Step], _Step]: ...
def then(phrase: str) -> Callable[[_Step], _Step]: ...
