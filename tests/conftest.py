"""Global test fixtures."""
from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

import pytest
import starlite_saqlalchemy
from starlite.testing import TestClient
from structlog.contextvars import clear_contextvars
from structlog.testing import CapturingLogger

from app import main

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any

    from pytest import MonkeyPatch
    from starlite import Starlite


@pytest.fixture(name="cap_logger")
def fx_capturing_logger(monkeypatch: MonkeyPatch) -> CapturingLogger:
    """Used to monkeypatch the app logger, so we can inspect output."""
    cap_logger = CapturingLogger()
    starlite_saqlalchemy.log.configure(
        starlite_saqlalchemy.log.default_processors  # type:ignore[arg-type]
    )
    # clear context for every test
    clear_contextvars()
    # pylint: disable=protected-access
    logger = starlite_saqlalchemy.log.controller.LOGGER.bind()
    logger._logger = cap_logger
    # drop rendering processor to get a dict, not bytes
    # noinspection PyProtectedMember
    logger._processors = starlite_saqlalchemy.log.default_processors[:-1]
    monkeypatch.setattr(starlite_saqlalchemy.log.controller, "LOGGER", logger)
    monkeypatch.setattr(starlite_saqlalchemy.log.worker, "LOGGER", logger)
    return cap_logger


@pytest.fixture(name="app")
def fx_app() -> Starlite:
    """Test application instance."""
    return main.create_app()


@pytest.fixture(name="client")
def fx_client(app: Starlite) -> Generator[TestClient, None, None]:
    """Test client fixture for making calls on the global app instance."""
    with TestClient(app=app) as client:
        yield client


@pytest.fixture()
def raw_authors() -> list[dict[str, Any]]:
    """

    Returns:
        Raw set of author data that can either be inserted into tables for integration tests, or
        used to create `Author` instances for unit tests.
    """
    return [
        {
            "id": UUID("97108ac1-ffcb-411d-8b1e-d9183399f63b"),
            "name": "Agatha Christie",
            "dob": date(1890, 9, 15),
            "created": datetime.min,
            "updated": datetime.min,
        },
        {
            "id": UUID("5ef29f3c-3560-4d15-ba6b-a2e5c721e4d2"),
            "name": "Leo Tolstoy",
            "dob": date(1828, 9, 9),
            "created": datetime.min,
            "updated": datetime.min,
        },
    ]
