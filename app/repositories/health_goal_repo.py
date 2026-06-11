from app.models.health_goal import HealthGoal
from app.repositories.base_repo import BaseRepository
from app.helpers.normalize import normalize_key


class HealthGoalRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)
        
    def _map_health_goal(self, record) -> HealthGoal:
        h = record["h"]

        return HealthGoal(
            id=h.get("id"),
            name=h.get("name"),
            key=h.get("key")
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (h:HealthGoal)
                RETURN h
            """)
            return [self._map_health_goal(r) for r in result]

        return self.read(_query)

    def get_by_id(self, health_goal_id: int):
        def _query(tx):
            result = tx.run("""
                MATCH (h:HealthGoal {id: $id})
                RETURN h
                LIMIT 1
            """, {"id": health_goal_id})

            record = result.single()
            return self._map_health_goal(record) if record else None
        return self.read(_query)
    
    def _find_by_key(self, key: str):
        
        _key = normalize_key(key)
        
        def query(tx):
            result = tx.run("""
                MATCH (h:HealthGoal {key: $key})
                RETURN h
                LIMIT 1
            """, {"key": _key})
            record = result.single()
            return self._map_health_goal(record) if record else None
        return self.read(query)

    def create(self, health_goal: HealthGoal):

        key = normalize_key(health_goal.name)

        health_goal_data = self.prepare_entity({
            "name": health_goal.name,
            "key": key
        })

        def _query(tx):
            result = tx.run("""
                OPTIONAL MATCH (exist:HealthGoal {key: $key})
                WITH exist
                WHERE exist IS NULL

                CREATE (h:HealthGoal $props)
                RETURN h
            """, {
                "key": key,
                "props": health_goal_data
            })

            record = result.single()
            return self._map_health_goal(record) if record else None

        return self.write(_query)
    
    def update(self, health_goal_id: int, name: str):

        key = normalize_key(name)

        def _query(tx):
            result = tx.run("""
                MATCH (h:HealthGoal {id: $id})

                WITH h, $key AS key, $name AS name, $id AS id

                WHERE NOT EXISTS {
                    MATCH (dup:HealthGoal {key: key})
                    WHERE dup.id <> id
                }

                SET h.name = name,
                    h.key = key

                RETURN h
            """, {
                "id": health_goal_id,
                "name": name,
                "key": key
            })

            record = result.single()
            return self._map_health_goal(record) if record else None

        return self.write(_query)

    def delete(self, health_goal_id: int):
        def _query(tx):
            tx.run("""
                MATCH (h:HealthGoal {id: $id})
                DETACH DELETE h
            """, {"id": health_goal_id})

            return True

        return self.write(_query)
