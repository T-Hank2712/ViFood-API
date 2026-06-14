from app.models.ingredient import Ingredient
from app.repositories.base_repo import BaseRepository
from app.helpers.slug import generate_key


class IngredientRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _map_ingredient(self, record) -> Ingredient:
        n = record["n"]

        return Ingredient(
            id=n.get("id"),
            name=n.get("name"),
            key=n.get("key"),
            description=n.get("description")
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Ingredient)
                RETURN n
            """)
            return [self._map_ingredient(r) for r in result]

        return self.read(_query)

    def get_by_id(self, ingredient_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Ingredient {id: $id})
                RETURN n
                LIMIT 1
            """, {"id": ingredient_id})

            record = result.single()
            return self._map_ingredient(record) if record else None

        return self.read(_query)

    def _find_by_key(self, key: str):

        _key = generate_key(key)

        def _query(tx):
            result = tx.run("""
                MATCH (n:Ingredient {key: $key})
                RETURN n
                LIMIT 1
            """, {"key": _key})

            record = result.single()
            return self._map_ingredient(record) if record else None

        return self.read(_query)

    def create(self, ingredient: Ingredient):

        key = generate_key(ingredient.name)

        ingredient_data = self.prepare_entity({
            "name": ingredient.name,
            "key": key,
            "description": ingredient.description
        })

        def _query(tx):
            result = tx.run("""
                OPTIONAL MATCH (exist:Ingredient {key: $key})
                WITH exist
                WHERE exist IS NULL

                CREATE (n:Ingredient $props)
                RETURN n
            """, {
                "key": key,
                "props": ingredient_data
            })

            record = result.single()
            return self._map_ingredient(record) if record else None

        return self.write(_query)

    def update(self, ingredient_id: str, ingredient: Ingredient):

        def _query(tx):
            result = tx.run("""
                MATCH (n:Ingredient {id: $id})
                SET n.name = $name,
                    n.description = $description,
                    n.key = $key
                RETURN n
            """, {
                "id": ingredient_id,
                "name": ingredient.name,
                "description": ingredient.description,
                "key": generate_key(ingredient.name)
            })

            record = result.single()
            return self._map_ingredient(record) if record else None

        return self.write(_query)

    def delete(self, ingredient_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Ingredient {id: $id})
                WITH n
                WHERE n IS NOT NULL
                DETACH DELETE n
                RETURN COUNT(n) > 0 AS deleted
            """, {"id": ingredient_id})

            record = result.single()
            return record["deleted"] if record else False

        return self.write(_query)

    def attach_effect(self, ingredient_id: str, effect_id: str):
        def _query(tx):
            tx.run("""
                MATCH (i:Ingredient {id: $ingredientId})
                MATCH (e:HealthEffect {id: $effectId})
                MERGE (i)-[:HAS_EFFECT]->(e)
            """, {
                "ingredientId": ingredient_id,
                "effectId": effect_id
            })

        return self.write(_query)

    def attach_category(self, ingredient_id: str, category_id: str):
        def _query(tx):
            tx.run("""
                MATCH (i:Ingredient {id: $ingredientId})
                MATCH (c:FoodCategory {id: $categoryId})
                MERGE (i)-[:IN_CATEGORY]->(c)
            """, {
                "ingredientId": ingredient_id,
                "categoryId": category_id
            })

        return self.write(_query)
