from app.models.food_category import FoodCategory
from app.repositories.base_repo import BaseRepository
from app.helpers.slug import generate_key


class FoodCategoryRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _map_food_category(self, record) -> FoodCategory:
        fc = record["fc"]

        return FoodCategory(
            id=fc.get("id"),
            name=fc.get("name"),
            key=fc.get("key")
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (fc:FoodCategory)
                RETURN fc
            """)
            return [self._map_food_category(r) for r in result]

        return self.read(_query)

    def get_by_id(self, category_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (fc:FoodCategory {id: $id})
                RETURN fc
                LIMIT 1
            """, {"id": category_id})

            record = result.single()
            return self._map_food_category(record) if record else None

        return self.read(_query)

    def _find_by_key(self, key: str):

        _key = generate_key(key)

        def _query(tx):
            result = tx.run("""
                MATCH (fc:FoodCategory {key: $key})
                RETURN fc
                LIMIT 1
            """, {"key": _key})

            record = result.single()
            return self._map_food_category(record) if record else None

        return self.read(_query)

    def create(self, category: FoodCategory):

        key = generate_key(category.name)

        category_data = self.prepare_entity({
            "name": category.name,
            "key": key
        })

        def _query(tx):
            result = tx.run("""
                OPTIONAL MATCH (exist:FoodCategory {key: $key})
                WITH exist
                WHERE exist IS NULL

                CREATE (fc:FoodCategory $props)
                RETURN fc
            """, {
                "key": key,
                "props": category_data
            })

            record = result.single()
            return self._map_food_category(record) if record else None

        return self.write(_query)

    def update(self, category_id: str, name: str):

        key = generate_key(name)

        def _query(tx):
            result = tx.run("""
                MATCH (fc:FoodCategory {id: $id})

                WITH fc, $key AS key, $name AS name, $id AS id

                WHERE NOT EXISTS {
                    MATCH (dup:FoodCategory {key: key})
                    WHERE dup.id <> id
                }

                SET fc.name = name,
                    fc.key = key

                RETURN fc
            """, {
                "id": category_id,
                "name": name,
                "key": key
            })

            record = result.single()
            return self._map_food_category(record) if record else None

        return self.write(_query)

    def delete(self, category_id: str):
        def _query(tx):
            tx.run("""
                MATCH (fc:FoodCategory {id: $id})
                DETACH DELETE fc
            """, {"id": category_id})

            return True

        return self.write(_query)
