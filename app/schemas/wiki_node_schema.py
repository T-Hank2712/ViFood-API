from pydantic import BaseModel, Field


class WikiNodeSection(BaseModel):
    section_type: str | None = None
    content: str


class WikiNodeResponse(BaseModel):
    id: str
    name: str
    sections: list[WikiNodeSection] = Field(default_factory=list)


class WikiNodeListApiResponse(BaseModel):
    message: str
    data: list[WikiNodeResponse]


class WikiNodeApiResponse(BaseModel):
    message: str
    data: WikiNodeResponse
