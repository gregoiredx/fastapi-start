import asyncio
import functools
from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Any
from typing import cast

from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import solve_dependencies
from fastapi.routing import run_endpoint_function
from starlette.requests import Request


def job(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Can be used as a decorator for a top level function to be run in a FastAPI like
    context.
    Especially usefull to resolve fastapi.Depends parameters and to run async functions
    seamlessly as FastApi endpoints are.

    Exemple usage:

    @job
    async def main(normal_param, service: Annotated[Service, Depends()]):
        ...

    if __name__ == "__main__":
        main(normal_param="a value")
    """

    @functools.wraps(func)
    def executor(**kwargs: dict[str, Any]) -> Any:
        loop = asyncio.get_event_loop()
        resolved_func = inject(func)
        loop.run_until_complete(resolved_func(**kwargs))

    return executor


def inject(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    async def resolved_func(**kwargs: dict[str, Any]) -> Any:
        async with AsyncExitStack() as exit_stack:
            return await _solve_and_run(exit_stack, func, **kwargs)

    return resolved_func


async def _solve_and_run(
    exit_stack: AsyncExitStack, func: Callable[..., Any], **kwargs: dict[str, Any]
) -> Any:
    dependant = get_dependant(path="", call=func)
    solved_result = await solve_dependencies(
        request=cast(Request, _JobRequest(exit_stack, kwargs)), dependant=dependant
    )
    values, errors, background_tasks, sub_response, _ = solved_result
    return await run_endpoint_function(
        dependant=dependant,
        values=values,
        is_coroutine=asyncio.iscoroutinefunction(dependant.call),
    )


class _JobRequest:
    def __init__(self, exit_stack: AsyncExitStack, params):
        self.scope = {
            "type": "job",
            "fastapi_astack": exit_stack,
        }
        self.query_params = params
        self.path_params: dict[str, Any] = {}
        self.headers: dict[str, Any] = {}
        self.cookies: dict[str, Any] = {}
