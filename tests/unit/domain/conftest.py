"""Fixtures for domain tests."""
from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

import pytest

from domain import authors

if TYPE_CHECKING:
    from typing import Any


@pytest.fixture(name="raw_author")
def fx_raw_author() -> dict[str, Any]:
    """Unstructured representation of an Author."""
    return {
        "name": "Some Author",
        "dob": date.min,
    }


@pytest.fixture(name="author")
def fx_author(raw_author: dict[str, Any]) -> authors.Author:
    """Structured and complete representation of an Author."""
    return authors.Author(id=uuid4(), created=datetime.min, updated=datetime.min, **raw_author)
