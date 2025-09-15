from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

class EventBase(BaseModel):
    title: str = Field(..., description="Title of the event")
    description: str = Field(..., description="Description of the event")
    start_time: datetime = Field(description="Start time (EST)")
    end_time: datetime = Field(description="End Time (EST)")
    location: str = Field(description="Either physical or virtual location")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Seminar of AI!",
                "description": "Detailed conversations about the impact of AI",
                "start_time": "2025-09-15T10:00:00Z",
                "end_time": "2025-09-15T12:00:00Z",
                "location": "Mudd Building Lobby",
            }
        }
    }

class EventCreate(EventBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Food Eating Competetion",
                "description": "Lets see who can eat the most hamburgers in a minute",
                "start_time": "2025-09-15T15:00:00Z",
                "end_time": "2025-09-15T17:00:00Z",
                "location": "Low Steps",
            }
        }
    }

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, json_schema_extra={"example": "Updated Event Title"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Updated description"})
    start_time: Optional[datetime] = Field(None, json_schema_extra={"example": "Updated start time: YYYY-MM-DDT00:00:00Z"})
    end_time: Optional[datetime] = Field(None, json_schema_extra={"example": "Updated end time: YYYY-MM-DDT00:00:00Z"})
    location: Optional[str] = Field(None, json_schema_extra={"example": "Zoom link / new room"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Updated Title"},
                {"location": "Zoom"},
                {"end_time": "2025-09-15T13:00:00Z"}
            ]
        }
    }

class EventRead(EventBase):
    id: UUID = Field(default_factory=uuid4, description="Server-generated UUID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last updated timestamp")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "77fb4ef8-b773-4393-9260-0d06e92b26aa",
                    "title": "AI Research Talk",
                    "description": "A seminar on the latest in AI research.",
                    "start_time": "2025-09-15T10:00:00Z",
                    "end_time": "2025-09-15T12:00:00Z",
                    "location": "Room 301, CS Building",
                    "created_at": "2025-09-01T12:00:00Z",
                    "updated_at": "2025-09-01T12:00:00Z"
                }
            ]
        }
    }