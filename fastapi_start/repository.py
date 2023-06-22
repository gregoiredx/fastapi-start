from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

from fastapi_start.database import Repository

mapper_registry = registry()


@mapper_registry.mapped_as_dataclass
class User:
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]


class UserRepository(Repository):
    def create_user(self, name: str) -> User:
        user = User(name)  # type: ignore[call-arg]
        self.session.add(user)
        self.session.flush((user,))
        return user

    def get_users(self) -> Sequence[User]:
        return self.session.scalars(select(User)).all()
