from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

class OrganizationBase(BaseModel):
    name: str = Field(..., description="Name of the organization")
    org_type: str = Field(..., description="Type of organization (College, company, club, etc.)")
    description: Optional[str] = Field(description="Summary of organization")
    website: Optional[str] = Field(desription="Official website")
    email: Optional[EmailStr] = Field(description="Email")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Columbia Computer Science",
                "org_type": "University",
                "description": "A top-tier computer science department.",
                "website": "https://www.cs.columbia.edu",
                "email": "info@cs.columbia.edu"
            }
        }
    }

class OrganizationCreate(OrganizationBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Cool Club",
                "org_type": "Club",
                "description": "we're the cool club. No further information need",
                "website": "coolclub.com",
                "email": "randomemail@gmail.om"
            }
        }
    }

class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, example="New Org Name")
    type: Optional[str] = Field(None, example="Company")
    description: Optional[str] = Field(None, example="Updated description")
    website: Optional[str] = Field(None, example="https://example.org")
    email: Optional[EmailStr] = Field(None, example="contact@example.org")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Updated Org name"},
                {"email": "new-contact@org.com"},
            ]
        }
    }

class OrganizationRead(OrganizationBase):
    id: UUID = Field(default_factory=uuid4, description="Organization ID", example="5c8ca863-7f20-4937-88a2-b4c2bde72d71")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Time of creation", example="2025-09-14T12:00:00Z")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Time of last update", example="2025-09-14T12:00:00Z")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "5c8ca863-7f20-4937-88a2-b4c2bde72d71",
                    "org_type": "club",
                    "name": "Random Name"
                }
            ]
        }
    }