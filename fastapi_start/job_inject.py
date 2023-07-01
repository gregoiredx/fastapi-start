from contextlib import ExitStack
from contextlib import contextmanager
from functools import partial

from fastapi.dependencies.utils import analyze_param
from fastapi.dependencies.utils import get_typed_signature
from fastapi.dependencies.utils import is_gen_callable


def inject(call):
    def enriched_call():
        with ExitStack() as exit_stack:
            return sub_inject(call, exit_stack)()

    return enriched_call


def sub_inject(call, exit_stack: ExitStack):
    endpoint_signature = get_typed_signature(call)
    signature_params = endpoint_signature.parameters
    injected_params = {}
    for param_name, param in signature_params.items():
        type_annotation, depends, param_field = analyze_param(
            param_name=param_name,
            annotation=param.annotation,
            value=param.default,
            is_path_param=False,
        )
        if depends and (dependency := depends.dependency):
            if is_gen_callable(dependency):
                injected_params[param_name] = exit_stack.enter_context(
                    contextmanager(sub_inject(dependency, exit_stack))()
                )
            else:
                injected_params[param_name] = sub_inject(dependency, exit_stack)()
    return partial(call, **injected_params)
