"""Books domain definitions."""
from __future__ import annotations

from typing import Annotated
from uuid import UUID  # noqa: TC003

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlite_saqlalchemy import db, dto, repository, service

from domain.authors import Author  # noqa: TC002


class Book(db.orm.Base):  # pylint: disable=too-few-public-methods
    """The Book domain object."""

    title: Mapped[str]
    author_id: Mapped[UUID] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Author] = relationship(
        lazy="joined", innerjoin=True, info=dto.field("read-only")
    )


class Repository(repository.sqlalchemy.SQLAlchemyRepository[Book]):
    """Book repository."""

    model_type = Book


class Service(service.Service[Book]):
    """Book service."""

    repository_type = Repository


ReadDTO = dto.FromMapped[Annotated[Book, "read"]]
"""
A pydantic model to serialize outbound `Book` representations.
"""
WriteDTO = dto.FromMapped[Annotated[Book, "write"]]
"""
A pydantic model to validate and deserialize `Book` creation/update data.
"""
