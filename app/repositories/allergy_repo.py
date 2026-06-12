from app.models.allergy import Allergy
from app.repositories.base_repo import BaseRepository
from app.helpers.slug import generate_key


class AllergyRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _map_allergy(self, record) -> Allergy:
        a = record["a"]

        return Allergy(
            id=a.get("id"),
            name=a.get("name"),
            key=a.get("key")
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (a:Allergy)
                RETURN a
            """)
            return [self._map_allergy(r) for r in result]

        return self.read(_query)

    def get_by_id(self, allergy_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (a:Allergy {id: $id})
                RETURN a
                LIMIT 1
            """, {"id": allergy_id})

            record = result.single()
            return self._map_allergy(record) if record else None

        return self.read(_query)

    def _find_by_key(self, key: str):

        _key = generate_key(key)

        def _query(tx):
            result = tx.run("""
                MATCH (a:Allergy {key: $key})
                RETURN a
                LIMIT 1
            """, {"key": _key})

            record = result.single()
            return self._map_allergy(record) if record else None

        return self.read(_query)

    def create(self, allergy: Allergy):

        key = generate_key(allergy.name)

        allergy_data = self.prepare_entity({
            "name": allergy.name,
            "key": key
        })

        def _query(tx):
            result = tx.run("""
                OPTIONAL MATCH (exist:Allergy {key: $key})
                WITH exist
                WHERE exist IS NULL

                CREATE (a:Allergy $props)
                RETURN a
            """, {
                "key": key,
                "props": allergy_data
            })

            record = result.single()
            return self._map_allergy(record) if record else None

        return self.write(_query)

    def update(self, allergy_id: str, name: str):

        key = generate_key(name)

        def _query(tx):
            result = tx.run("""
                MATCH (a:Allergy {id: $id})

                WITH a, $key AS key, $name AS name, $id AS id

                WHERE NOT EXISTS {
                    MATCH (dup:Allergy {key: key})
                    WHERE dup.id <> id
                }

                SET a.name = name,
                    a.key = key

                RETURN a
            """, {
                "id": allergy_id,
                "name": name,
                "key": key
            })

            record = result.single()
            return self._map_allergy(record) if record else None

        return self.write(_query)

    def delete(self, allergy_id: str):
        def _query(tx):
            tx.run("""
                MATCH (a:Allergy {id: $id})
                DETACH DELETE a
            """, {"id": allergy_id})

            return True

        return self.write(_query)
