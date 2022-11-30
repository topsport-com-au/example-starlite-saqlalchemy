"""Authors domain definitions."""
from __future__ import annotations

import asyncio
from datetime import date  # noqa: TC003
from typing import TYPE_CHECKING, Annotated

from sqlalchemy.orm import Mapped  # noqa: TC002
from starlite_saqlalchemy import db, dto, repository, service
from structlog.contextvars import bind_contextvars

if TYPE_CHECKING:
    from typing import Any


class Author(db.orm.Base):  # pylint: disable=too-few-public-methods
    """The Author domain object."""

    name: Mapped[str]
    dob: Mapped[date]


class Repository(repository.sqlalchemy.SQLAlchemyRepository[Author]):
    """Author repository."""

    model_type = Author


class Service(service.Service[Author]):
    """Author service object."""

    repository_type = Repository

    async def create(self, data: Author) -> Author:
        created = await super().create(data)
        await self.enqueue_background_task(
            "receive_created_author", raw_author=ReadDTO.from_orm(created).dict()
        )
        return data

    async def receive_created_author(self, raw_author: dict[str, Any]) -> None:
        """Async callback for new authors.

        Args:
            raw_author: Unstructured representation of created author.
        """
        bind_contextvars(author=raw_author)
        # do something with the new author
        await asyncio.sleep(0.5)


WriteDTO = dto.FromMapped[Annotated[Author, "write"]]
"""
A pydantic model to validate `Author` create/update data.
"""

ReadDTO = dto.FromMapped[Annotated[Author, "read"]]
"""
A pydantic model to serialize outbound `Author` representations.
"""
