from app.repositories.base_repo import BaseRepository
from app.schemas.wiki_node_schema import WikiNodeResponse, WikiNodeSection


class NutrientRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _map_wiki_node(self, record) -> WikiNodeResponse:
        return WikiNodeResponse(
            id=record["id"],
            name=record["name"],
            sections=[
                WikiNodeSection(
                    section_type=section.get("section_type"),
                    content=section.get("content"),
                )
                for section in record.get("sections", [])
                if section and section.get("content")
            ],
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient)
                OPTIONAL MATCH (n)-[:HAS_WIKI_PROFILE]->(profile:WikiProfile)
                OPTIONAL MATCH (profile)-[:HAS_SECTION]->(section:WikiSection)
                WITH n, profile, section
                ORDER BY section.order ASC
                WITH
                    n,
                    profile,
                    [
                        item IN collect({
                            section_type: section.section_type,
                            content: section.content
                        })
                        WHERE item.content IS NOT NULL
                    ] AS sections
                RETURN
                    n.id AS id,
                    coalesce(n.name_vi, profile.title, n.name) AS name,
                    sections
                ORDER BY name
            """)
            return [self._map_wiki_node(r) for r in result]

        return self.read(_query)

    def get_by_id(self, nutrient_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient {id: $id})
                OPTIONAL MATCH (n)-[:HAS_WIKI_PROFILE]->(profile:WikiProfile)
                OPTIONAL MATCH (profile)-[:HAS_SECTION]->(section:WikiSection)
                WITH n, profile, section
                ORDER BY section.order ASC
                WITH
                    n,
                    profile,
                    [
                        item IN collect({
                            section_type: section.section_type,
                            content: section.content
                        })
                        WHERE item.content IS NOT NULL
                    ] AS sections
                RETURN
                    n.id AS id,
                    coalesce(n.name_vi, profile.title, n.name) AS name,
                    sections
                LIMIT 1
            """, {"id": nutrient_id})

            record = result.single()
            return self._map_wiki_node(record) if record else None

        return self.read(_query)
