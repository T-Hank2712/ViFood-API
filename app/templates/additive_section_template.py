from app.schemas.additive_v1_schema import (
    AdditiveDetailResponse,
    AdditiveSectionResponse,
)


def build_additive_sections(additive: AdditiveDetailResponse) -> list[AdditiveSectionResponse]:
    return [
        AdditiveSectionResponse(
            section_type="overview",
            title=f"{_display_name(additive)} là gì?",
            content=_build_overview(additive),
        ),
        AdditiveSectionResponse(
            section_type="food_role",
            title="Vai trò trong thực phẩm",
            content=_build_food_role(additive),
        ),
        AdditiveSectionResponse(
            section_type="permitted_foods",
            title=f"{_display_name(additive)} được dùng trong những thực phẩm nào?",
            content=_build_permitted_foods(additive),
        ),
        AdditiveSectionResponse(
            section_type="sources_and_regulations",
            title="Nguồn thông tin và quy định tham khảo",
            content=_build_sources_and_regulations(additive),
        ),
    ]


def _display_name(additive: AdditiveDetailResponse) -> str:
    return additive.name_vi or additive.name or additive.id


def _english_name(additive: AdditiveDetailResponse) -> str | None:
    if additive.name and additive.name != additive.name_vi:
        return additive.name
    return None


def _alias_names(additive: AdditiveDetailResponse) -> list[str]:
    aliases = [
        alias.name
        for alias in additive.aliases
        if alias.name
    ]

    if additive.ins:
        aliases.insert(0, f"INS {additive.ins}")

    return list(dict.fromkeys(aliases))


def _function_names(additive: AdditiveDetailResponse) -> list[str]:
    return list(dict.fromkeys(
        function.name[:1].lower() + function.name[1:]
        for function in additive.functions
        if function.name
    ))


def _category_names(additive: AdditiveDetailResponse, limit: int = 8) -> list[str]:
    names = [
        category.name_vi or category.name
        for category in additive.permitted_categories
        if category.name_vi or category.name
    ]
    return list(dict.fromkeys(names))[:limit]


def _build_overview(additive: AdditiveDetailResponse) -> str:
    name = _display_name(additive)
    if additive.ins:
        sentences = [f"{name} là một phụ gia thực phẩm có mã INS {additive.ins}."]
    else:
        sentences = [f"{name} là một phụ gia thực phẩm được ghi nhận trong dữ liệu phụ gia của ViFood."]

    english_name = _english_name(additive)
    if english_name:
        sentences.append(f"Tên tiếng Anh thường gặp của chất này là {english_name}.")

    aliases = _alias_names(additive)
    if aliases:
        sentences.append(f"Trên nhãn thực phẩm, chất này cũng có thể được ghi dưới các tên như {', '.join(aliases)}.")

    functions = _function_names(additive)
    if functions:
        sentences.append(f"Trong thực phẩm, phụ gia này thường được dùng với vai trò {', '.join(functions)}.")

    return " ".join(sentences)


def _build_food_role(additive: AdditiveDetailResponse) -> str:
    name = _display_name(additive)
    functions = _function_names(additive)

    if functions:
        return (
            f"{name} có thể đóng vai trò là {', '.join(functions)}. "
            "Nhờ các vai trò này, phụ gia có thể hỗ trợ đặc tính cảm quan, cấu trúc hoặc độ ổn định của sản phẩm, "
            "tùy theo loại thực phẩm và mục đích sử dụng."
        )

    return (
        f"Dữ liệu hiện tại chưa ghi nhận chức năng cụ thể của {name}. "
        "Khi đọc nhãn thực phẩm, người dùng nên đối chiếu tên phụ gia hoặc mã INS với nguồn quy định liên quan."
    )


def _build_permitted_foods(additive: AdditiveDetailResponse) -> str:
    name = _display_name(additive)
    categories = _category_names(additive)

    if categories:
        return (
            f"{name} có thể được sử dụng trong một số nhóm thực phẩm nhất định theo quy định về phụ gia thực phẩm. "
            f"Các nhóm thực phẩm được ghi nhận gồm "
            f"{', '.join(categories)}. "
            "Việc sử dụng trong từng sản phẩm cụ thể còn phụ thuộc vào nhóm thực phẩm, mục đích sử dụng và giới hạn được quy định."
        )

    return (
        f"Dữ liệu hiện tại chưa ghi nhận nhóm thực phẩm cụ thể được phép sử dụng {name}. "
        "Cần đối chiếu thêm văn bản quy định hoặc tiêu chuẩn phụ gia thực phẩm liên quan."
    )


def _build_sources_and_regulations(additive: AdditiveDetailResponse) -> str:
    name = _display_name(additive)
    sentences: list[str] = []

    regulation_names = [
        regulation.name
        for regulation in additive.regulations
        if regulation.name
    ]

    source_names = [
        source.name
        for source in additive.sources
        if source.name
    ]
    if source_names or regulation_names:
        references = list(dict.fromkeys(source_names + regulation_names))
        sentences.append(
            f"Thông tin về {name} được tham khảo từ "
            f"{', '.join(references)}."
        )

    if regulation_names:
        sentences.append(
            "Người dùng có thể tham khảo thêm các văn bản này để biết phụ gia được phép dùng "
            "trong nhóm thực phẩm nào và các điều kiện sử dụng liên quan."
        )

    source_details: list[str] = []

    if additive.raw_page_number:
        source_details.append(f"trang {additive.raw_page_number}")

    if additive.raw_record_number:
        source_details.append(f"bản ghi số {additive.raw_record_number}")

    if additive.reviewed_at:
        source_details.insert(0, f"Thông tin đã được rà soát vào ngày {additive.reviewed_at}")

    if source_details:
        sentences.append(", ".join(source_details) + " của nguồn dữ liệu.")

    if not sentences:
        return "Dữ liệu hiện tại chưa có nguồn thông tin hoặc quy định tham khảo chi tiết cho phụ gia này."

    return " ".join(sentences)
