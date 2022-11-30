"""Application entrypoint.

Example:

    `uvicorn app.main:app`
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from starlite import Starlite
from starlite_saqlalchemy import ConfigureApp, settings

from app.controllers import authors, books

if TYPE_CHECKING:
    from typing import Any


def create_app() -> Starlite:
    """Application factory."""
    plugin = ConfigureApp()
    kwargs: dict[str, Any] = {}
    if settings.app.ENVIRONMENT == "production":
        kwargs["openapi_config"] = None
    return Starlite(
        route_handlers=[authors.create_router(), books.create_router()],
        on_app_init=[plugin],
        **kwargs,
    )
