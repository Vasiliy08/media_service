from datetime import datetime

from typing import Any, Generic, Literal, TypeVar
from uuid import UUID
from pydantic import BaseModel, Field


TData = TypeVar("TData")
TListItem = TypeVar("TListItem")


class ErrorSchema(BaseModel):
    error: str


class Files(BaseModel):
    uuid: UUID
    original_name: str
    size: int
    file_format: str
    extension: str
    last_downloaded: datetime


class PaginationIn(BaseModel):
    offset: int = 0
    limit: int = 5
    order_by: Literal["asc", "desc"] = "asc"


class PaginationOut(BaseModel):
    page: int
    limit: int
    total: int
    order_by: Literal["asc", "desc"]


class ListPaginatedResponse(BaseModel, Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOut


class ApiResponse(BaseModel, Generic[TData]):
    data: TData | dict = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)