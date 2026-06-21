from app.models.health_goal import HealthGoal
from app.repositories.health_goal_repo import HealthGoalRepository
from app.schemas.name_schema import NameRequest


class HealthGoalServiceV1:

    def __init__(self, db):
        self.repo = HealthGoalRepository(db)

    def get_all_health_goals(self):
        health_goal = self.repo.get_all()
        
        if not health_goal:
            raise ValueError("Health Goal Not Found")
        
        return health_goal

    def get_health_goal_by_id(self, health_goal_id: int):
        health_goal = self.repo.get_by_id(health_goal_id)
        
        if not health_goal:
            raise ValueError("Health Goal Not Found")
        return health_goal

    def create_health_goal(self, name: str):
        existing = self.repo._find_by_key(name)

        if existing:
            raise ValueError("Health Goal already exist")

        health_goal = HealthGoal(name=name)
        return self.repo.create(health_goal)

    def update_health_goal(self, health_goal_id: int, name: str):
        health_goal = self.repo.get_by_id(health_goal_id)

        if not health_goal:
            raise ValueError("Health Goal not found")

        existing = self.repo._find_by_key(name)
        if existing:
            raise ValueError("Health Goal already exist")

        return self.repo.update(health_goal_id, name)

    def delete_health_goal(self, health_goal_id: int):
        health_goal = self.repo.get_by_id(health_goal_id)

        if not health_goal:
            raise ValueError("Health Goal not found")

        success = self.repo.delete(health_goal_id)

        return success
    
    def create_many_health_goals(self, requests: list[NameRequest]):
        created = []

        for req in requests:
            existing = self.repo._find_by_key(req.name)

            if existing:
                continue

            health_goal = HealthGoal(
                name=req.name
            )

            created_health_goal = self.repo.create(health_goal)

            if created_health_goal:
                created.append(created_health_goal)

        if not created:
            raise ValueError("All health goals already exist or nothing was created")

        return created
