from pydantic import BaseModel

from app.schemas.wiki_node_schema import WikiNodeSection


class SearchNodeResponse(BaseModel):
    id: str
    name: str
    type: str
    sections: list[WikiNodeSection]


class SearchNodeListApiResponse(BaseModel):
    message: str
    data: list[SearchNodeResponse]


class SearchNodeApiResponse(BaseModel):
    message: str
    data: SearchNodeResponse
