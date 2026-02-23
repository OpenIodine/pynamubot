"""
Typed request and response schema definitions for TheSeedAPI.

This module defines multiple `TypedDict` classes that describe the
expected structure of JSON request bodies and response payloads
when interacting with TheSeedAPI using the `requests` library.

Each class is meant to serve as a static typing adi for improved
editor support, validation, and readability in API-related code.

See <https://doc.theseed.io/> for full API documentation.
"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class EditGETResponse(BaseModel):
    text: str = Field(description="The content of the document")
    exists: bool = Field(description="Whether the document exists")
    token: str = Field(description="The edit token (will be used for edit POST request)")


class EditPOSTBody(BaseModel):
    text: str = Field(description="The edited document text")
    log: str = Field(description="Edit summary")
    token: str = Field(description="The edit token (from edit GET request)")


class EditPOSTResponse(BaseModel):
    status: str = Field(description="The status of the edit operation")
    rev: int = Field(description="The edited revision")


class Namespaces(BaseModel):
    namespace: str = Field(description="The namespace of the document")
    count: int = Field(description="The number of documents in the namespace")


class Backlinks(BaseModel):
    document: str = Field(description="The document linked to")
    flags: str = Field(description="Linking flags")


class BacklinkResponse(BaseModel):
    namespaces: list[Namespaces] = Field(description="List of namespaces")
    backlinks: list[Backlinks] = Field(description="List of backlinks")
    fromm: Optional[str] = Field(description="Starting point for the query")
    until: Optional[str] = Field(description="Ending point for the query")


class DiscussResponse(BaseModel):
    slug: str = Field(description="The discussion slug")
    topic: str = Field(description="The discussion topic")
    updated_date: datetime = Field(description="The last comment's Unix timestamp")
    status: Literal["normal", "close", "pause"] = Field(description="The discussion status")
