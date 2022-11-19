"""Unittest specific config/fixtures."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from starlite_saqlalchemy import worker
from starlite_saqlalchemy.testing import GenericMockRepository

from domain import authors

if TYPE_CHECKING:
    from typing import Any
    from uuid import UUID

    from pytest import MonkeyPatch


@pytest.fixture(autouse=True)
def _patch_worker(monkeypatch: MonkeyPatch) -> None:
    """We don't want the worker to start for unittests."""

    async def _startup_mock(_: Any) -> None:
        ...

    monkeypatch.setattr(worker.Worker, "on_app_startup", _startup_mock)


@pytest.fixture(autouse=True)
def _author_repository(raw_authors: list[dict[str, Any]], monkeypatch: pytest.MonkeyPatch) -> None:
    AuthorRepository = GenericMockRepository[authors.Author]
    collection: dict[UUID, authors.Author] = {}
    for raw_author in raw_authors:
        author = authors.Author(**raw_author)
        collection[getattr(author, AuthorRepository.id_attribute)] = author
    monkeypatch.setattr(AuthorRepository, "collection", collection)
    monkeypatch.setattr(authors.Service, "repository_type", AuthorRepository)
