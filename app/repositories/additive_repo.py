from app.models.additive import Additive
from app.repositories.base_repo import BaseRepository
from app.schemas.additive_schema import AdditiveDetail
from app.models.health_effect import HealthEffect
from app.models.food_category import FoodCategory
from app.helpers.slug import generate_key


class AdditiveRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _map_additive(self, record) -> Additive:
        n = record["n"]

        return Additive(
            id=n.get("id"),
            name=n.get("name"),
            key=n.get("key"),
            code=n.get("code"),
            description=n.get("description")
        )
        
    def _map_additive_detail(self, record) -> AdditiveDetail:
        a = record["a"]

        return AdditiveDetail(
            id=a.get("id"),
            name=a.get("name"),
            key=a.get("key"),
            code=a.get("code"),
            description=a.get("description"),
            effects=[
                HealthEffect(
                    id=e.get("id"),
                    title=e.get("title"),
                    key=e.get("key"),
                    description=e.get("description")
                )
                for e in record.get("effects", [])
                if e and e.get("id")
            ],
            categories=[
                FoodCategory(
                    id=c.get("id"),
                    name=c.get("name"),
                    key=c.get("key")
                )
                for c in record.get("categories", [])
                if c and c.get("id")
            ]
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Additive)
                RETURN n
            """)
            return [self._map_additive(r) for r in result]

        return self.read(_query)

    def get_by_id(self, additive_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Additive {id: $id})
                RETURN n
                LIMIT 1
            """, {"id": additive_id})

            record = result.single()
            return self._map_additive(record) if record else None

        return self.read(_query)
    
    def get_additive_detail(self, additive_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (a:Additive {id: $id})

                OPTIONAL MATCH (a)-[:HAS_EFFECT]->(e:HealthEffect)
                WITH a,
                    COLLECT(DISTINCT e) AS effects

                OPTIONAL MATCH (a)-[:IN_CATEGORY]->(c:FoodCategory)
                WITH a,
                    effects,
                    COLLECT(DISTINCT c) AS categories

                RETURN a, effects, categories
            """, {"id": additive_id})

            record = result.single()
            return self._map_additive_detail(record) if record else None

        return self.read(_query)

    def _find_by_key(self, key: str):

        _key = generate_key(key)

        def _query(tx):
            result = tx.run("""
                MATCH (n:Additive {key: $key})
                RETURN n
                LIMIT 1
            """, {"key": _key})

            record = result.single()
            return self._map_additive(record) if record else None

        return self.read(_query)

    def create(self, additive: Additive):

        key = generate_key(additive.name)

        additive_data = self.prepare_entity({
            "name": additive.name,
            "key": key,
            "code": additive.code,
            "description": additive.description
        })

        def _query(tx):
            result = tx.run("""
                OPTIONAL MATCH (exist:Additive {key: $key})
                WITH exist
                WHERE exist IS NULL

                CREATE (n:Additive $props)
                RETURN n
            """, {
                "key": key,
                "props": additive_data
            })

            record = result.single()
            return self._map_additive(record) if record else None

        return self.write(_query)

    def update(self, additive_id: str, additive: Additive):

        def _query(tx):
            result = tx.run("""
                MATCH (n:Additive {id: $id})
                SET n.name = $name,
                    n.description = $description,
                    n.key = $key,
                    n.code = $code
                RETURN n
            """, {
                "id": additive_id,
                "name": additive.name,
                "description": additive.description,
                "key": generate_key(additive.name),
                "code": additive.code
            })

            record = result.single()
            return self._map_additive(record) if record else None

        return self.write(_query)

    def delete(self, additive_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Additive {id: $id})
                WITH n
                WHERE n IS NOT NULL
                DETACH DELETE n
                RETURN COUNT(n) > 0 AS deleted
            """, {"id": additive_id})

            record = result.single()
            return record["deleted"] if record else False

        return self.write(_query)

    def attach_effect(self, additive_id: str, effect_id: str):
        def _query(tx):
            tx.run("""
                MATCH (a:Additive {id: $additiveId})
                MATCH (e:HealthEffect {id: $effectId})
                MERGE (a)-[:HAS_EFFECT]->(e)
            """, {
                "additiveId": additive_id,
                "effectId": effect_id
            })

        return self.write(_query)

    def attach_category(self, additive_id: str, category_id: str):
        def _query(tx):
            tx.run("""
                MATCH (a:Additive {id: $additiveId})
                MATCH (c:FoodCategory {id: $categoryId})
                MERGE (a)-[:IN_CATEGORY]->(c)
            """, {
                "additiveId": additive_id,
                "categoryId": category_id
            })

        return self.write(_query)
