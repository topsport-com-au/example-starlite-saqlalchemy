"""Tests for Authors controllers."""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from unittest.mock import ANY, AsyncMock, MagicMock

from starlite.status_codes import HTTP_200_OK, HTTP_201_CREATED
from starlite_saqlalchemy.db import async_session_factory

import app
import domain.authors

if TYPE_CHECKING:
    from pytest import MonkeyPatch
    from starlite.testing import TestClient


def test_service_provider(monkeypatch: MonkeyPatch) -> None:
    """Test service dependency provider."""
    service_mock = MagicMock()
    monkeypatch.setattr(app.controllers.authors, "Service", service_mock)
    session = async_session_factory()
    app.controllers.authors.provides_service(session)
    service_mock.assert_called_once_with(session=session)


def test_get_authors(client: TestClient) -> None:
    """Test authors collection controller."""
    resp = client.get("/authors")
    assert resp.status_code == HTTP_200_OK
    assert resp.json() == [
        {
            "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
            "created": "0001-01-01T00:00:00",
            "updated": "0001-01-01T00:00:00",
            "name": "Agatha Christie",
            "dob": "1890-09-15",
        },
        {
            "id": "5ef29f3c-3560-4d15-ba6b-a2e5c721e4d2",
            "created": "0001-01-01T00:00:00",
            "updated": "0001-01-01T00:00:00",
            "name": "Leo Tolstoy",
            "dob": "1828-09-09",
        },
    ]


def test_create_author(client: TestClient, monkeypatch: MonkeyPatch) -> None:
    """Test create author controller."""
    enqueue_mock = AsyncMock()
    monkeypatch.setattr(domain.authors.Service, "enqueue_background_task", enqueue_mock)
    resp = client.post("/authors", json={"name": "Joe Blogs", "dob": "2022-11-17"})
    assert resp.status_code == HTTP_201_CREATED
    assert resp.json() == {
        "id": ANY,
        "created": ANY,
        "updated": ANY,
        "name": "Joe Blogs",
        "dob": "2022-11-17",
    }
    enqueue_mock.assert_called_once_with(
        "receive_created_author",
        raw_author={
            "id": ANY,
            "created": ANY,
            "updated": ANY,
            "name": "Joe Blogs",
            "dob": datetime.date(2022, 11, 17),
        },
    )


def test_get_author(client: TestClient) -> None:
    """Test get author controller."""
    resp = client.get("/authors/97108ac1-ffcb-411d-8b1e-d9183399f63b")
    assert resp.status_code == HTTP_200_OK
    assert resp.json() == {
        "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
        "created": "0001-01-01T00:00:00",
        "updated": "0001-01-01T00:00:00",
        "name": "Agatha Christie",
        "dob": "1890-09-15",
    }


def test_update_author(client: TestClient) -> None:
    """Test update author controller."""
    resp = client.put(
        "/authors/97108ac1-ffcb-411d-8b1e-d9183399f63b",
        json={"name": "Aggy Christie", "dob": "1890-09-15"},
    )
    assert resp.status_code == HTTP_200_OK
    assert resp.json() == {
        "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
        "created": "0001-01-01T00:00:00",
        "updated": ANY,
        "name": "Aggy Christie",
        "dob": "1890-09-15",
    }


def test_delete_author(client: TestClient) -> None:
    """Test delete author controller."""
    resp = client.delete("/authors/97108ac1-ffcb-411d-8b1e-d9183399f63b")
    assert resp.status_code == HTTP_200_OK
    assert resp.json() == {
        "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
        "created": "0001-01-01T00:00:00",
        "updated": "0001-01-01T00:00:00",
        "name": "Agatha Christie",
        "dob": "1890-09-15",
    }
