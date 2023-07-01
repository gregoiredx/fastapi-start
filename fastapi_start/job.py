import logging
from typing import Annotated

from fastapi import Depends

from fastapi_start.fast_api_job import job
from fastapi_start.repository import UserRepository
from fastapi_start.settings import Settings
from fastapi_start.settings import get_settings

logger = logging.getLogger(__name__)


@job
async def create_user(
    name,
    settings: Annotated[Settings, Depends(get_settings)],
    user_repository: Annotated[UserRepository, Depends()],
):
    logger.error(
        f"Hello from job {name} {settings.db_url} {user_repository.get_users()}"
    )
    user_repository.create_user(name)


if __name__ == "__main__":
    create_user(name="John Job")
