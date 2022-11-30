"""Tests for authors domain."""
from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

import pytest
from starlite_saqlalchemy.testing import GenericMockRepository

from domain import authors

if TYPE_CHECKING:
    from typing import Any

    from pytest import MonkeyPatch


@pytest.fixture(name="service")
def fx_service(monkeypatch: MonkeyPatch) -> authors.Service:
    """Authors service, with repository type patched to mock repo."""
    monkeypatch.setattr(authors.Service, "repository_type", GenericMockRepository[authors.Author])
    return authors.Service()


async def test_service_create_enqueues_background_task(
    raw_author: dict[str, Any], service: authors.Service, monkeypatch: MonkeyPatch
) -> None:
    """Test ensures that creating an author enqueues the async callback."""
    mock = AsyncMock()
    monkeypatch.setattr(service, "enqueue_background_task", mock)
    author = await service.create(authors.WriteDTO(**raw_author).to_mapped())
    mock.assert_called_once_with(
        "receive_created_author", raw_author=authors.ReadDTO.from_orm(author).dict()
    )


async def test_receive_created_author(raw_author: dict[str, Any], service: authors.Service) -> None:
    """Test doesn't do anything, because the method doesn't really do
    anything!"""
    await service.receive_created_author(raw_author)
