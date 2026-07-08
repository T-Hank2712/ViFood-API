from pydantic import BaseModel, Field


class NutrientNodeResponse(BaseModel):
    id: str
    name: str | None = None
    name_vi: str | None = None
    external_code: str | None = None
    default_unit: str | None = None
    vietnam_label_requirement: str | None = None
    source_version: str | None = None
    status: str | None = None
    reviewed_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class NutrientSourceResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    source_type: str | None = None
    url: str | None = None
    status: str | None = None
    reviewed_at: str | None = None


class NutrientHealthClaimResponse(BaseModel):
    id: str | None = None
    claim_text: str | None = None
    evidence_excerpt: str | None = None
    evidence_level: str | None = None
    conditions_of_use: str | None = None
    status: str | None = None
    reviewed_at: str | None = None


class NutrientSectionResponse(BaseModel):
    section_type: str
    title: str
    content: str


class NutrientDetailResponse(NutrientNodeResponse):
    sources: list[NutrientSourceResponse] = Field(default_factory=list, exclude=True)
    health_claims: list[NutrientHealthClaimResponse] = Field(default_factory=list, exclude=True)
    sections: list[NutrientSectionResponse] = Field(default_factory=list)


class NutrientListApiResponse(BaseModel):
    message: str
    data: list[NutrientNodeResponse]


class NutrientDetailApiResponse(BaseModel):
    message: str
    data: NutrientDetailResponse
