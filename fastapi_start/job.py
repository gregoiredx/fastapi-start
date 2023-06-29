import logging
from contextlib import ExitStack
from contextlib import contextmanager
from functools import partial
from typing import Annotated

from fastapi import Depends
from fastapi.dependencies.utils import analyze_param
from fastapi.dependencies.utils import get_typed_signature
from fastapi.dependencies.utils import is_gen_callable

from fastapi_start.repository import UserRepository
from fastapi_start.settings import Settings
from fastapi_start.settings import get_settings


def inject(call):
    endpoint_signature = get_typed_signature(call)
    signature_params = endpoint_signature.parameters
    injected_params = {}
    gen_injected_params = {}
    for param_name, param in signature_params.items():
        type_annotation, depends, param_field = analyze_param(
            param_name=param_name,
            annotation=param.annotation,
            value=param.default,
            is_path_param=False,
        )
        dependency = depends.dependency
        if is_gen_callable(dependency):
            gen_injected_params[param_name] = contextmanager(inject(dependency))()
        else:
            injected_params[param_name] = inject(dependency)()
    with ExitStack() as stack:
        return partial(
            call,
            **injected_params,
            **{
                param_name: stack.enter_context(gen_injected_param)
                for param_name, gen_injected_param in gen_injected_params.items()
            },
        )


logger = logging.getLogger()


@inject
def main(
    settings: Annotated[Settings, Depends(get_settings)],
    user_repository: Annotated[UserRepository, Depends()],
):
    logger.error(f"Hello from job {settings.db_url} {user_repository.get_users()}")


if __name__ == "__main__":
    main()
