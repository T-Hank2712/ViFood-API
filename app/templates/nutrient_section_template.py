from app.schemas.nutrient_v1_schema import (
    NutrientDetailResponse,
    NutrientSectionResponse,
)


def build_nutrient_sections(nutrient: NutrientDetailResponse) -> list[NutrientSectionResponse]:
    return [
        NutrientSectionResponse(
            section_type="overview",
            title="Tổng quan",
            content=_build_overview(nutrient),
        ),
        NutrientSectionResponse(
            section_type="common_unit",
            title="Đơn vị thường dùng",
            content=_build_common_unit(nutrient),
        ),
        NutrientSectionResponse(
            section_type="health_note",
            title="Vai trò / lưu ý sức khỏe",
            content=_build_health_note(nutrient),
        ),
        NutrientSectionResponse(
            section_type="sources_and_labeling",
            title="Ghi nhãn và nguồn tham khảo",
            content=_build_sources_and_labeling(nutrient),
        ),
    ]


def _display_name(nutrient: NutrientDetailResponse) -> str:
    return nutrient.name_vi or nutrient.name or nutrient.id


def _english_name(nutrient: NutrientDetailResponse) -> str | None:
    if nutrient.name and nutrient.name != nutrient.name_vi:
        return nutrient.name
    return None


def _build_overview(nutrient: NutrientDetailResponse) -> str:
    name = _display_name(nutrient)
    sentences = [
        f"{name} là một chất dinh dưỡng được ghi nhận trong dữ liệu nutrient của ViFood."
    ]

    english_name = _english_name(nutrient)
    if english_name:
        sentences.append(f"Tên tiếng Anh hoặc tên quốc tế thường gặp là {english_name}.")

    if nutrient.external_code:
        sentences.append(f"Mã định danh trong bộ dữ liệu là {nutrient.external_code}.")

    if nutrient.source_version:
        sentences.append(f"Phiên bản nguồn dữ liệu: {nutrient.source_version}.")

    return " ".join(sentences)


def _build_common_unit(nutrient: NutrientDetailResponse) -> str:
    name = _display_name(nutrient)

    if nutrient.default_unit:
        return (
            f"{name} thường được ghi theo đơn vị {nutrient.default_unit}. "
            "Đơn vị này giúp đối chiếu hàm lượng chất dinh dưỡng trên nhãn thực phẩm "
            "hoặc trong bảng thành phần thực phẩm."
        )

    return (
        f"Dữ liệu hiện tại chưa ghi nhận đơn vị mặc định cho {name}. "
        "Khi hiển thị trên nhãn hoặc bảng thành phần, cần đối chiếu theo nguồn dữ liệu cụ thể."
    )


def _build_health_note(nutrient: NutrientDetailResponse) -> str:
    name = _display_name(nutrient)

    if nutrient.health_claims:
        claim_texts = [
            _strip_sentence_end(claim.claim_text)
            for claim in nutrient.health_claims
            if claim.claim_text
        ]
        claim_summary = "; ".join(claim_texts)

        if claim_summary:
            return (
                f"Dữ liệu sức khỏe liên quan đến {name} ghi nhận: {claim_summary}. "
                "Nội dung này chỉ nên được xem là thông tin tham khảo về dinh dưỡng và sức khỏe cộng đồng, "
                "không phải chẩn đoán, điều trị, hay khuyến nghị thay thế ý kiến của chuyên gia y tế."
            )

    return (
        f"Hiện dữ liệu chưa có ghi nhận riêng về vai trò hoặc lưu ý sức khỏe cho {name}. "
        "Người dùng nên đọc thông tin này như dữ liệu tham khảo khi xem nhãn thực phẩm, "
        "không xem như tư vấn y khoa cá nhân."
    )


def _build_sources_and_labeling(nutrient: NutrientDetailResponse) -> str:
    name = _display_name(nutrient)
    sentences: list[str] = []

    if nutrient.vietnam_label_requirement:
        sentences.append(
            f"Trạng thái yêu cầu ghi nhãn dinh dưỡng tại Việt Nam của {name}: "
            f"{_label_requirement_text(nutrient.vietnam_label_requirement)}."
        )

    source_names = [
        source.name
        for source in nutrient.sources
        if source.name
    ]
    if source_names:
        sentences.append("Nguồn tham khảo gồm " + ", ".join(source_names) + ".")

    if nutrient.reviewed_at:
        sentences.append(f"Ngày rà soát dữ liệu: {nutrient.reviewed_at}.")

    if not sentences:
        return f"Dữ liệu hiện tại chưa có nguồn tham khảo chi tiết cho {name}."

    return " ".join(sentences)


def _strip_sentence_end(value: str) -> str:
    return value.strip().rstrip(".")


def _label_requirement_text(value: str) -> str:
    mapping = {
        "required": "bắt buộc",
        "conditional": "có điều kiện",
        "optional": "không bắt buộc",
    }
    return mapping.get(value, value)
