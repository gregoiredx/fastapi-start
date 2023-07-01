import functools
from collections.abc import Callable
from contextlib import ExitStack
from contextlib import contextmanager
from inspect import Parameter
from typing import Any

from fastapi.dependencies.utils import analyze_param
from fastapi.dependencies.utils import get_typed_signature
from fastapi.dependencies.utils import is_gen_callable


def inject(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def resolved_func(*args: Any, **kwargs: dict[str, Any]) -> Any:
        with ExitStack() as exit_stack:
            return _call(_inject(func, exit_stack), exit_stack, *args, **kwargs)

    return resolved_func


def _inject(func: Callable[..., Any], exit_stack: ExitStack) -> Callable[..., Any]:
    return functools.partial(
        func,
        **{
            param.name: _call(_inject(dependency, exit_stack), exit_stack)
            for param in get_typed_signature(func).parameters.values()
            if (dependency := _get_param_dependency(param))
        },
    )


def _call(
    func: Callable[..., Any],
    exit_stack: ExitStack,
    *args: Any,
    **kwargs: dict[str, Any],
) -> Any:
    return (
        exit_stack.enter_context(contextmanager(func)(*args, **kwargs))
        if is_gen_callable(func)
        else func(*args, **kwargs)
    )


def _get_param_dependency(param: Parameter) -> Callable[..., Any] | None:
    _, depends, _ = analyze_param(
        param_name=param.name,
        annotation=param.annotation,
        value=param.default,
        is_path_param=False,
    )
    return depends.dependency if depends else None
