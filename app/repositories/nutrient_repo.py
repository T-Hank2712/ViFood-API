from app.models.nutrient import Nutrient
from app.repositories.base_repo import BaseRepository
from app.helpers.slug import generate_key


class NutrientRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)
        
    def _map_nutrient(self, record) -> Nutrient:
        n = record["n"]

        return Nutrient(
            id=n.get("id"),
            name=n.get("name"),
            key=n.get("key"),
            description=n.get("description")
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient)
                RETURN n
            """)
            return [self._map_nutrient(r) for r in result]

        return self.read(_query)

    def get_by_id(self, allergy_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient {id: $id})
                RETURN n
                LIMIT 1
            """, {"id": allergy_id})

            record = result.single()
            return self._map_nutrient(record) if record else None

        return self.read(_query)
    
    def _find_by_key(self, key: str):
        
        _key = generate_key(key)
        
        def query(tx):
            result = tx.run("""
                MATCH (h:Nutrient {key: $key})
                RETURN h
                LIMIT 1
            """, {"key": _key})
            record = result.single()
            return self._map_nutrient(record) if record else None
        return self.read(query)

    def create(self, nutrient: Nutrient):

        key = generate_key(nutrient.name)

        nutrient_data = self.prepare_entity({
            "name": nutrient.name,
            "key": key,
            "description": nutrient.description
        })

        def _query(tx):
            result = tx.run("""
                OPTIONAL MATCH (exist:Nutrient {key: $key})
                WITH exist
                WHERE exist IS NULL

                CREATE (n:Nutrient $props)
                RETURN n
            """, {
                "key": key,
                "props": nutrient_data
            })

            record = result.single()
            return self._map_nutrient(record) if record else None

        return self.write(_query)
    
    def update(self, nutrient_id: str, nutrient: Nutrient):

        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient {id: $id})
                SET n.name = $name,
                    n.description = $description,
                    n.key = $key
                RETURN n
            """, {
                "id": nutrient_id,
                "name": nutrient.name,
                "description": nutrient.description,
                "key": generate_key(nutrient.name)
            })

            record = result.single()
            return self._map_nutrient(record) if record else None

        return self.write(_query)

    def delete(self, nutrient_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient {id: $id})
                WITH n
                WHERE n IS NOT NULL
                DETACH DELETE n
                RETURN COUNT(n) > 0 AS deleted
            """, {"id": nutrient_id})

            record = result.single()
            return record["deleted"] if record else False

        return self.write(_query)
    
    def attach_effects(self, nutrient_id: str, effects: list[str]):
        def _query(tx):
            tx.run("""
                MATCH (n:Nutrient {id: $nutrientId})
                UNWIND $effects AS effectId
                MATCH (eNode:HealthEffect {id: effectId})
                MERGE (n)-[:HAS_EFFECT]->(eNode)
            """, {
                "nutrientId": nutrient_id,
                "effects": effects
            })

        return self.write(_query)

    def attach_categories(self, nutrient_id: str, categories: list[str]):
        def _query(tx):
            tx.run("""
                MATCH (n:Nutrient {id: $nutrientId})
                UNWIND $categories AS categoryId
                MATCH (cNode:FoodCategory {id: categoryId})
                MERGE (n)-[:IN_CATEGORY]->(cNode)
            """, {
                "nutrientId": nutrient_id,
                "categories": categories
            })

        return self.write(_query)
