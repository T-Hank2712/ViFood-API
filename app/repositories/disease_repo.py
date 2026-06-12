from app.models.disease import Disease
from app.repositories.base_repo import BaseRepository
from app.helpers.slug import generate_key


class DiseaseRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _map_disease(self, record) -> Disease:
        d = record["d"]

        return Disease(
            id=d.get("id"),
            name=d.get("name"),
            key=d.get("key")
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (d:Disease)
                RETURN d
            """)
            return [self._map_disease(r) for r in result]

        return self.read(_query)

    def get_by_id(self, disease_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (d:Disease {id: $id})
                RETURN d
                LIMIT 1
            """, {"id": disease_id})

            record = result.single()
            return self._map_disease(record) if record else None

        return self.read(_query)

    def _find_by_key(self, key: str):

        _key = generate_key(key)

        def _query(tx):
            result = tx.run("""
                MATCH (d:Disease {key: $key})
                RETURN d
                LIMIT 1
            """, {"key": _key})

            record = result.single()
            return self._map_disease(record) if record else None

        return self.read(_query)

    def create(self, disease: Disease):

        key = generate_key(disease.name)

        disease_data = self.prepare_entity({
            "name": disease.name,
            "key": key
        })

        def _query(tx):
            result = tx.run("""
                OPTIONAL MATCH (exist:Disease {key: $key})
                WITH exist
                WHERE exist IS NULL

                CREATE (d:Disease $props)
                RETURN d
            """, {
                "key": key,
                "props": disease_data
            })

            record = result.single()
            return self._map_disease(record) if record else None

        return self.write(_query)

    def update(self, disease_id: str, name: str):

        key = generate_key(name)

        def _query(tx):
            result = tx.run("""
                MATCH (d:Disease {id: $id})

                WITH d, $key AS key, $name AS name, $id AS id

                WHERE NOT EXISTS {
                    MATCH (dup:Disease {key: key})
                    WHERE dup.id <> id
                }

                SET d.name = name,
                    d.key = key

                RETURN d
            """, {
                "id": disease_id,
                "name": name,
                "key": key
            })

            record = result.single()
            return self._map_disease(record) if record else None

        return self.write(_query)

    def delete(self, disease_id: str):
        def _query(tx):
            tx.run("""
                MATCH (d:Disease {id: $id})
                DETACH DELETE d
            """, {"id": disease_id})

            return True

        return self.write(_query)
