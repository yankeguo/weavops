from typing import Any

from pydantic import BaseModel


class ChangesetCreateItem(BaseModel):
    key: list[str]
    val: Any  # pyright: ignore[reportExplicitAny]


class ChangesetUpdateItem(BaseModel):
    key: list[str]
    val: Any  # pyright: ignore[reportExplicitAny]


class ChangesetDeleteItem(BaseModel):
    key: list[str]


class ChangesetModel(BaseModel):
    create: list[ChangesetCreateItem]
    update: list[ChangesetUpdateItem]
    delete: list[ChangesetDeleteItem]
