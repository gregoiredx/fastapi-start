import asyncio
import logging
from typing import Annotated

from fastapi import Depends

from fastapi_start.job_inject import inject
from fastapi_start.repository import UserRepository
from fastapi_start.settings import Settings
from fastapi_start.settings import get_settings

logger = logging.getLogger(__name__)


@inject
async def main(
    normal_param,
    settings: Annotated[Settings, Depends(get_settings)],
    user_repository: Annotated[UserRepository, Depends()],
):
    logger.error(
        f"Hello from job {normal_param} {settings.db_url} {user_repository.get_users()}"
    )
    user_repository.create_user("John Job")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(normal_param="normal param"))
