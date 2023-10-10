from __future__ import annotations

from typing import Callable

from typing_extensions import TypeAlias

from .runner import Context

_ThreeArgStep: TypeAlias = Callable[[Context, str, str, str], None]
_TwoArgStep: TypeAlias = Callable[[Context, str, str], None]
_OneArgStep: TypeAlias = Callable[[Context, str], None]
_NoArgStep: TypeAlias = Callable[[Context], None]
_Step: TypeAlias = _NoArgStep | _OneArgStep | _TwoArgStep | _ThreeArgStep

def given(phrase: str) -> Callable[[_Step], _Step]: ...
def when(phrase: str) -> Callable[[_Step], _Step]: ...
def then(phrase: str) -> Callable[[_Step], _Step]: ...
