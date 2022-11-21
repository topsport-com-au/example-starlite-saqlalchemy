"""Books domain definitions."""
from __future__ import annotations

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
        lazy="joined", innerjoin=True, info={"dto": dto.Attrib(mark=dto.Mark.READ_ONLY)}
    )


class Repository(repository.sqlalchemy.SQLAlchemyRepository[Book]):
    """Book repository."""

    model_type = Book


class Service(service.Service[Book]):
    """Book service."""

    repository_type = Repository


ReadDTO = dto.factory("BookReadDTO", Book, purpose=dto.Purpose.READ)
"""
A pydantic model to serialize outbound `Book` representations.
"""
WriteDTO = dto.factory("BookWriteDTO", Book, purpose=dto.Purpose.WRITE)
"""
A pydantic model to validate and deserialize `Book` creation/update data.
"""
