Sprint Completion Status Report
**Student	Name:**	[Emanuel Pimentel]
**Sprint	Number:**	[Sprint	0]
**Duration:**	[9/13/25]	– [9/14/2025]
**Report	Date:**	[9/14/2025]


1. Sprint Goal 🎯
**Defined	Goal:**	
- Clone	Professor	Ferguson’s Simple	Microservices	Repository.
- Create	a	project	that	is	my	version	using	two	different	resources.
  - Copy	the	structure	of	Professor	Ferguson’s	repository
  - Define	two	models.
  - Implement	“API	first” definition	by	implementing	placeholder	routes	for	
    each	resource:
    - GET	/<resource>
    - POST	/<resource>
    - GET	/<resource>/{id}
    - PUT /<resource>/{id}
    - DELETE /<resource>/{id}
  - Annotate	models	and	paths	to	autogenerate	OpenAPI	document.
  - Tested	OpenAPI	document	dispatching	to	methods.


**Outcome:**	[Achieved]

2. Completed Work ✅
Resource 1
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

Resource 2
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

main.py Routes
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

OpenAPI Document (Partial)
<img width="968" height="807" alt="Screenshot 2025-09-14 205338" src="https://github.com/user-attachments/assets/0c306d82-c859-46e7-aead-3355455badaa" />
<img width="973" height="705" alt="Screenshot 2025-09-14 205346" src="https://github.com/user-attachments/assets/0c90a8c4-852c-4498-96f7-0a351b412651" />

Link to Recording of Demo
https://youtu.be/3w3c_k68YNo
