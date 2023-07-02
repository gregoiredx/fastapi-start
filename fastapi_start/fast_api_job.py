"""
Can be used to run functions in a FastAPI like context.
Especially usefull to resolve fastapi.Depends parameters and to run async functions
seamlessly as FastApi endpoints are.

Exemple usage:
```
# my_app/jobs.py

app = FastApiJob()

@app.job
async def hello(name: str, service: Annotated[Service, Depends()]):
    print(f"Hello {name}!")
    await service.run()

if __name__ == "__main__":
    app.run()
```

can be run with `python -m my_app.jobs hello world`
"""
import asyncio
import functools
import inspect
from collections.abc import Callable
from contextlib import AsyncExitStack
from sys import argv
from typing import Any
from typing import cast

from fastapi import FastAPI
from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import solve_dependencies
from fastapi.routing import run_endpoint_function
from starlette.requests import Request


class FastApiJob(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jobs = {}

    def job(self, func: Callable[..., Any]) -> Callable[..., Any]:
        self.jobs[func.__name__] = func
        return func

    def run(self, *args):
        if not args:
            args = argv[1:]
        job_name = args[0]
        func = self.jobs[job_name]
        bound_params = inspect.signature(func).bind_partial(*args[1:])
        bound_params.apply_defaults()
        loop = asyncio.get_event_loop()
        resolved_func = _inject(self, func)
        loop.run_until_complete(resolved_func(**bound_params.arguments))


def _inject(app: FastApiJob, func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    async def resolved_func(**kwargs: dict[str, Any]) -> Any:
        async with AsyncExitStack() as exit_stack:
            return await _solve_and_run(app, exit_stack, func, **kwargs)

    return resolved_func


async def _solve_and_run(
    app: FastApiJob,
    exit_stack: AsyncExitStack,
    func: Callable[..., Any],
    **kwargs: dict[str, Any]
) -> Any:
    dependant = get_dependant(path="", call=func)
    solved_result = await solve_dependencies(
        request=cast(Request, _JobRequest(exit_stack, kwargs)),
        dependant=dependant,
        dependency_overrides_provider=app,
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
