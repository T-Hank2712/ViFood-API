from pydantic import BaseModel, Field


class AdditiveNodeResponse(BaseModel):
    id: str
    name: str | None = None
    name_vi: str | None = None
    ins: str | None = None
    status: str | None = None
    raw_page_number: int | None = None
    raw_record_number: int | None = None
    reviewed_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AdditiveAliasResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    alias_type: str | None = None
    language: str | None = None


class AdditiveFunctionResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    language: str | None = None


class AdditiveFoodCategoryResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    name_vi: str | None = None
    regulatory_food_group_code: str | None = None


class AdditiveRegulationResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    document_number: str | None = None
    issued_on: str | None = None
    status: str | None = None
    reviewed_at: str | None = None


class AdditiveSourceResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    source_type: str | None = None
    url: str | None = None
    status: str | None = None
    reviewed_at: str | None = None


class AdditiveSectionResponse(BaseModel):
    section_type: str
    title: str
    content: str


class AdditiveDetailResponse(AdditiveNodeResponse):
    aliases: list[AdditiveAliasResponse] = Field(default_factory=list, exclude=True)
    functions: list[AdditiveFunctionResponse] = Field(default_factory=list, exclude=True)
    permitted_categories: list[AdditiveFoodCategoryResponse] = Field(default_factory=list, exclude=True)
    regulations: list[AdditiveRegulationResponse] = Field(default_factory=list, exclude=True)
    sources: list[AdditiveSourceResponse] = Field(default_factory=list, exclude=True)
    sections: list[AdditiveSectionResponse] = Field(default_factory=list)


class AdditiveListApiResponse(BaseModel):
    message: str
    data: list[AdditiveNodeResponse]


class AdditiveDetailApiResponse(BaseModel):
    message: str
    data: AdditiveDetailResponse
