"""Test application and factory."""
from __future__ import annotations

from typing import TYPE_CHECKING

import starlite_saqlalchemy

from app import main

if TYPE_CHECKING:
    from pytest import MonkeyPatch


def test_no_openapi_config_in_prod(monkeypatch: MonkeyPatch) -> None:
    """Test that prod apps aren't configuring openapi docs."""
    monkeypatch.setattr(starlite_saqlalchemy.settings.app, "ENVIRONMENT", "production")
    assert main.create_app().openapi_config is None


def test_openapi_config_in_dev(monkeypatch: MonkeyPatch) -> None:
    """Test that dev apps are configuring openapi docs."""
    monkeypatch.setattr(starlite_saqlalchemy.settings.app, "ENVIRONMENT", "development")
    assert main.create_app().openapi_config is not None
