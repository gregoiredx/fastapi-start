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
            return _inject_and_call(exit_stack, func, *args, **kwargs)

    return resolved_func


def _inject_and_call(
    exit_stack: ExitStack,
    func: Callable[..., Any],
    *args: Any,
    **kwargs: dict[str, Any],
) -> Any:
    resolved_depends_params = {
        param.name: _inject_and_call(exit_stack, dependency)
        for param in get_typed_signature(func).parameters.values()
        if (dependency := _get_param_dependency(param))
    }
    resolved_func = functools.partial(func, **resolved_depends_params)
    if is_gen_callable(resolved_func):
        return exit_stack.enter_context(contextmanager(resolved_func)(*args, **kwargs))
    return resolved_func(*args, **kwargs)


def _get_param_dependency(param: Parameter) -> Callable[..., Any] | None:
    _, depends, _ = analyze_param(
        param_name=param.name,
        annotation=param.annotation,
        value=param.default,
        is_path_param=False,
    )
    return depends.dependency if depends else None
