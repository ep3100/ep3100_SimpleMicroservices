from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health
from models.event import EventCreate, EventRead, EventUpdate
from models.organization import OrganizationCreate, OrganizationRead, OrganizationUpdate


port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
events: Dict[UUID, EventRead] = {}
organizations: Dict[UUID, EventRead] = {}

app = FastAPI(
    title="Person/Address API",
    description="Demo FastAPI app using Pydantic v2 models for Person and Address",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]


# -----------------------------------------------------------------------------
# Event endpoints
# -----------------------------------------------------------------------------
@app.post("/events", response_model=EventRead, status_code=201)
def create_event(event: EventCreate):
    event_read = EventRead(**event.model_dump())
    events[event_read.id]= event_read
    return event_read

@app.get("/events", response_model=List[EventRead])
def list_events(
    title: Optional[str] = Query(None, description="Filter by title substring"),
    upcoming: Optional[bool] = Query(False, description="Show future events only"),
): 
    result = list(events.values())

    if title is not None:
        result = [a for a in result if title.lower() in a.title.lower()]

    if upcoming is not None:
        now = datetime.utcnow()
        result = [a for a in result if a.start_time > now]

    return result


@app.get("/events/{event_id}", response_model=EventRead)
def get_event(event_id: UUID):
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    return events[event_id]


@app.patch("/events/{event_id}", response_model=EventRead)
def update_event(event_id: UUID, update: EventUpdate):
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    stored = events[event_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    stored["updated_at"] = datetime.utcnow()
    events[event_id] = EventRead(**stored)
    return events[event_id]


@app.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: UUID):
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    del events[event_id]



# -----------------------------------------------------------------------------
# Organization endpoints
# -----------------------------------------------------------------------------
@app.post("/organizations", response_model=OrganizationRead, status_code=201)
def create_organization(org: OrganizationCreate):
    org_read = OrganizationRead(**org.model_dump())
    organizations[org_read.id] = org_read
    return org_read

@app.get("/organizations", response_model=List[OrganizationRead])
def list_organizations():
    return list(organizations.values())

@app.get("/organizations/{org_id}", response_model=OrganizationRead)
def get_organization(org_id: UUID):
    if org_id not in organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organizations[org_id]


@app.patch("/organizations/{org_id}", response_model=OrganizationRead)
def update_organization(org_id: UUID, update: OrganizationUpdate):
    if org_id not in organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    stored = organizations[org_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    stored["updated_at"] = datetime.utcnow()
    organizations[org_id] = OrganizationRead(**stored)
    return organizations[org_id]


@app.delete("/organizations/{org_id}", status_code=204)
def delete_organization(org_id: UUID):
    if org_id not in organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    del organizations[org_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
