from app.models.health_effect import HealthEffect
from app.repositories.base_repo import BaseRepository
from app.helpers.slug import generate_key


class HealthEffectRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _map_health_effect(self, record) -> HealthEffect:
        he = record["he"]

        return HealthEffect(
            id=he.get("id"),
            name=he.get("name"),
            key=he.get("key"),
            description=he.get("description")
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (he:HealthEffect)
                RETURN he
            """)
            return [self._map_health_effect(r) for r in result]

        return self.read(_query)

    def get_by_id(self, effect_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (he:HealthEffect {id: $id})
                RETURN he
                LIMIT 1
            """, {"id": effect_id})

            record = result.single()
            return self._map_health_effect(record) if record else None

        return self.read(_query)

    def _find_by_key(self, key: str):

        _key = generate_key(key)

        def _query(tx):
            result = tx.run("""
                MATCH (he:HealthEffect {key: $key})
                RETURN he
                LIMIT 1
            """, {"key": _key})

            record = result.single()
            return self._map_health_effect(record) if record else None

        return self.read(_query)

    def create(self, health_effect: HealthEffect):

        key = generate_key(health_effect.name)

        effect_data = self.prepare_entity({
            "name": health_effect.name,
            "key": key,
            "description": health_effect.description
        })

        def _query(tx):
            result = tx.run("""
                OPTIONAL MATCH (exist:HealthEffect {key: $key})
                WITH exist
                WHERE exist IS NULL

                CREATE (he:HealthEffect $props)
                RETURN he
            """, {
                "key": key,
                "props": effect_data
            })

            record = result.single()
            return self._map_health_effect(record) if record else None

        return self.write(_query)

    def update(
        self,
        effect_id: str,
        name: str,
        description: str
    ):

        key = generate_key(name)

        def _query(tx):
            result = tx.run("""
                MATCH (he:HealthEffect {id: $id})

                WITH he, $key AS key, $name AS name,
                     $description AS description,
                     $id AS id

                WHERE NOT EXISTS {
                    MATCH (dup:HealthEffect {key: key})
                    WHERE dup.id <> id
                }

                SET he.name = name,
                    he.key = key,
                    he.description = description

                RETURN he
            """, {
                "id": effect_id,
                "name": name,
                "key": key,
                "description": description
            })

            record = result.single()
            return self._map_health_effect(record) if record else None

        return self.write(_query)

    def delete(self, effect_id: str):
        def _query(tx):
            tx.run("""
                MATCH (he:HealthEffect {id: $id})
                DETACH DELETE he
            """, {"id": effect_id})

            return True

        return self.write(_query)
