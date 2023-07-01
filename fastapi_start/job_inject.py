import functools
from collections.abc import Callable
from contextlib import ExitStack
from contextlib import contextmanager
from inspect import Parameter
from typing import Any

from fastapi.dependencies.utils import analyze_param
from fastapi.dependencies.utils import get_typed_signature
from fastapi.dependencies.utils import is_gen_callable


def inject(call):
    @functools.wraps(call)
    def enriched_call():
        with ExitStack() as exit_stack:
            return sub_inject(call, exit_stack)()

    return enriched_call


def sub_inject(call, exit_stack: ExitStack):
    return functools.partial(
        call,
        **{
            param.name: _resolve_dependency(dependency, exit_stack)
            for param in get_typed_signature(call).parameters.values()
            if (dependency := _get_param_dependency(param))
        },
    )


def _get_param_dependency(param: Parameter) -> Callable[..., Any] | None:
    _, depends, _ = analyze_param(
        param_name=param.name,
        annotation=param.annotation,
        value=param.default,
        is_path_param=False,
    )
    return depends.dependency if depends else None


def _resolve_dependency(dependency: Callable[..., Any], exit_stack: ExitStack) -> Any:
    if is_gen_callable(dependency):
        return exit_stack.enter_context(
            contextmanager(sub_inject(dependency, exit_stack))()
        )
    return sub_inject(dependency, exit_stack)()
