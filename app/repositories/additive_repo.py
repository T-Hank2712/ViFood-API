from app.repositories.base_repo import BaseRepository
from app.schemas.additive_v1_schema import (
    AdditiveAliasResponse,
    AdditiveDetailResponse,
    AdditiveFoodCategoryResponse,
    AdditiveFunctionResponse,
    AdditiveNodeResponse,
    AdditiveRegulationResponse,
    AdditiveSourceResponse,
)


class AdditiveRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _to_string(self, value) -> str | None:
        return str(value) if value is not None else None

    def _map_additive_node(self, node) -> AdditiveNodeResponse:
        return AdditiveNodeResponse(
            id=node.get("id"),
            name=node.get("name"),
            name_vi=node.get("name_vi"),
            ins=node.get("ins"),
            status=node.get("status"),
            raw_page_number=node.get("raw_page_number"),
            raw_record_number=node.get("raw_record_number"),
            reviewed_at=self._to_string(node.get("reviewed_at")),
            created_at=self._to_string(node.get("created_at")),
            updated_at=self._to_string(node.get("updated_at")),
        )

    def _map_alias(self, node) -> AdditiveAliasResponse | None:
        if not node or not node.get("id"):
            return None

        return AdditiveAliasResponse(
            id=node.get("id"),
            name=node.get("name"),
            alias_type=node.get("alias_type"),
            language=node.get("language"),
        )

    def _map_function(self, node) -> AdditiveFunctionResponse | None:
        if not node or not node.get("id"):
            return None

        return AdditiveFunctionResponse(
            id=node.get("id"),
            name=node.get("name"),
            language=node.get("language"),
        )

    def _map_category(self, node) -> AdditiveFoodCategoryResponse | None:
        if not node or not node.get("id"):
            return None

        return AdditiveFoodCategoryResponse(
            id=node.get("id"),
            name=node.get("name"),
            name_vi=node.get("name_vi"),
            regulatory_food_group_code=node.get("regulatory_food_group_code"),
        )

    def _map_regulation(self, node) -> AdditiveRegulationResponse | None:
        if not node or not node.get("id"):
            return None

        return AdditiveRegulationResponse(
            id=node.get("id"),
            name=node.get("name"),
            document_number=node.get("document_number"),
            issued_on=self._to_string(node.get("issued_on")),
            status=node.get("status"),
            reviewed_at=self._to_string(node.get("reviewed_at")),
        )

    def _map_source(self, node) -> AdditiveSourceResponse | None:
        if not node or not node.get("id"):
            return None

        return AdditiveSourceResponse(
            id=node.get("id"),
            name=node.get("name"),
            source_type=node.get("source_type"),
            url=node.get("url"),
            status=node.get("status"),
            reviewed_at=self._to_string(node.get("reviewed_at")),
        )

    def _map_detail(self, record) -> AdditiveDetailResponse:
        additive = self._map_additive_node(record["a"])

        return AdditiveDetailResponse(
            **additive.model_dump(),
            aliases=[
                alias
                for alias in (self._map_alias(node) for node in record.get("aliases", []))
                if alias
            ],
            functions=[
                function
                for function in (self._map_function(node) for node in record.get("functions", []))
                if function
            ],
            permitted_categories=[
                category
                for category in (self._map_category(node) for node in record.get("categories", []))
                if category
            ],
            regulations=[
                regulation
                for regulation in (self._map_regulation(node) for node in record.get("regulations", []))
                if regulation
            ],
            sources=[
                source
                for source in (self._map_source(node) for node in record.get("sources", []))
                if source
            ],
        )

    def get_all(self) -> list[AdditiveNodeResponse]:
        def _query(tx):
            result = tx.run("""
                MATCH (a:Additive)
                RETURN a
                ORDER BY coalesce(a.name_vi, a.name, a.id)
            """)
            return [self._map_additive_node(record["a"]) for record in result]

        return self.read(_query)

    def get_by_id(self, additive_id: str) -> AdditiveDetailResponse | None:
        def _query(tx):
            result = tx.run("""
                MATCH (a:Additive {id: $id})
                OPTIONAL MATCH (a)-[:REFERS_TO]->(alias:Alias)
                WITH a, collect(DISTINCT alias) AS aliases
                OPTIONAL MATCH (a)-[:HAS_FUNCTION]->(function:FunctionalClass)
                WITH a, aliases, collect(DISTINCT function) AS functions
                OPTIONAL MATCH (a)-[:PERMITTED_IN]->(category:FoodCategory)
                WITH a, aliases, functions, collect(DISTINCT category) AS categories
                OPTIONAL MATCH (a)<-[:GOVERNS]-(regulation:Regulation)
                WITH a, aliases, functions, categories, collect(DISTINCT regulation) AS regulations
                OPTIONAL MATCH (a)-[:SUPPORTED_BY]->(source:Source)
                RETURN
                    a,
                    aliases,
                    functions,
                    categories,
                    regulations,
                    collect(DISTINCT source) AS sources
                LIMIT 1
            """, {"id": additive_id})

            record = result.single()
            return self._map_detail(record) if record else None

        return self.read(_query)
