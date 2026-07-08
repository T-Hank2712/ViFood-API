from app.repositories.base_repo import BaseRepository
from app.schemas.nutrient_v1_schema import (
    NutrientDetailResponse,
    NutrientHealthClaimResponse,
    NutrientNodeResponse,
    NutrientSourceResponse,
)


class NutrientRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _map_nutrient_node(self, node) -> NutrientNodeResponse:
        return NutrientNodeResponse(
            id=node.get("id"),
            name=node.get("name"),
            name_vi=node.get("name_vi"),
            external_code=node.get("external_code"),
            default_unit=node.get("default_unit"),
            vietnam_label_requirement=node.get("vietnam_label_requirement"),
            source_version=node.get("source_version"),
            status=node.get("status"),
            reviewed_at=node.get("reviewed_at"),
            created_at=node.get("created_at"),
            updated_at=node.get("updated_at"),
        )

    def _map_source(self, source) -> NutrientSourceResponse | None:
        if not source or not source.get("id"):
            return None

        return NutrientSourceResponse(
            id=source.get("id"),
            name=source.get("name"),
            source_type=source.get("source_type"),
            url=source.get("url"),
            status=source.get("status"),
            reviewed_at=source.get("reviewed_at"),
        )

    def _map_health_claim(self, claim) -> NutrientHealthClaimResponse | None:
        if not claim or not claim.get("id"):
            return None

        return NutrientHealthClaimResponse(
            id=claim.get("id"),
            claim_text=claim.get("claim_text"),
            evidence_excerpt=claim.get("evidence_excerpt"),
            evidence_level=claim.get("evidence_level"),
            conditions_of_use=claim.get("conditions_of_use"),
            status=claim.get("status"),
            reviewed_at=claim.get("reviewed_at"),
        )

    def _map_nutrient_detail(self, record) -> NutrientDetailResponse:
        nutrient = self._map_nutrient_node(record["n"])

        sources = [
            source
            for source in (
                self._map_source(source_node)
                for source_node in record.get("sources", [])
            )
            if source
        ]
        health_claims = [
            claim
            for claim in (
                self._map_health_claim(claim_node)
                for claim_node in record.get("health_claims", [])
            )
            if claim
        ]

        return NutrientDetailResponse(
            **nutrient.model_dump(),
            sources=sources,
            health_claims=health_claims,
        )

    def get_all(self) -> list[NutrientNodeResponse]:
        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient)
                RETURN n
                ORDER BY coalesce(n.name_vi, n.name, n.id)
            """)
            return [self._map_nutrient_node(record["n"]) for record in result]

        return self.read(_query)

    def get_by_id(self, nutrient_id: str) -> NutrientDetailResponse | None:
        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient {id: $id})
                OPTIONAL MATCH (n)-[:SUPPORTED_BY]->(source:Source)
                WITH n, collect(DISTINCT source) AS sources
                OPTIONAL MATCH (n)<-[:SUBJECT_OF]-(claim:HealthClaim)
                RETURN
                    n,
                    sources,
                    collect(DISTINCT claim) AS health_claims
                LIMIT 1
            """, {"id": nutrient_id})

            record = result.single()
            return self._map_nutrient_detail(record) if record else None

        return self.read(_query)
