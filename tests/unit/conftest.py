"""Unittest specific config/fixtures."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from starlite_saqlalchemy import worker
from starlite_saqlalchemy.testing import GenericMockRepository

from domain import authors

if TYPE_CHECKING:
    from typing import Any

    from pytest import MonkeyPatch


@pytest.fixture(autouse=True)
def _patch_worker(monkeypatch: MonkeyPatch) -> None:
    """We don't want the worker to start for unittests."""

    async def _startup_mock(_: Any) -> None:
        ...

    monkeypatch.setattr(worker.Worker, "on_app_startup", _startup_mock)


@pytest.fixture(autouse=True)
def _author_repository(raw_authors: list[dict[str, Any]], monkeypatch: pytest.MonkeyPatch) -> None:
    repo = GenericMockRepository[authors.Author]
    repo.seed_collection([authors.Author(**raw_author) for raw_author in raw_authors])
    monkeypatch.setattr(authors.Service, "repository_type", repo)
