"""Controllers for books domain."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlite import Dependency, Parameter, Provide, Router, delete, get, post, put
from starlite.status_codes import HTTP_200_OK
from starlite_saqlalchemy.repository.filters import CollectionFilter
from starlite_saqlalchemy.repository.types import FilterTypes

from domain.books import Book, ReadDTO, Service, WriteDTO

DETAIL_ROUTE = "/{book_id:uuid}"


def provides_service(db_session: AsyncSession) -> Service:
    """Constructs repository and service objects for the request."""
    return Service(session=db_session)


@get()
async def get_books(
    service: Service,
    author_ids: list[UUID] | None = Parameter(default=None, query="author"),
    filters: list[FilterTypes] = Dependency(skip_validation=True),
) -> list[ReadDTO]:
    """Get a list of books."""
    if author_ids:
        filters.append(CollectionFilter("author_id", author_ids))
    return [ReadDTO.from_orm(item) for item in await service.list(*filters)]


@post()
async def create_book(data: WriteDTO, service: Service) -> ReadDTO:
    """Create a `Book`."""
    return ReadDTO.from_orm(await service.create(Book.from_dto(data)))


@get(DETAIL_ROUTE)
async def get_book(service: Service, book_id: UUID) -> ReadDTO:
    """Get Book by ID."""
    return ReadDTO.from_orm(await service.get(book_id))


@put(DETAIL_ROUTE)
async def update_book(data: WriteDTO, service: Service, book_id: UUID) -> ReadDTO:
    """Update a book."""
    return ReadDTO.from_orm(await service.update(book_id, Book.from_dto(data)))


@delete(DETAIL_ROUTE, status_code=HTTP_200_OK)
async def delete_book(service: Service, book_id: UUID) -> ReadDTO:
    """Delete Book by ID."""
    return ReadDTO.from_orm(await service.delete(book_id))


def create_router() -> Router:
    """Create a router for the /books domain."""
    return Router(
        path="/books",
        route_handlers=[get_books, create_book, get_book, update_book, delete_book],
        dependencies={"service": Provide(provides_service)},
        tags=["Books"],
    )
