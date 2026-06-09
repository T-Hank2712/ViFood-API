from app.models.health_goal import HealthGoal
from app.db import db
from app.repositories.health_goal_repo import HealthGoalRepository


class HealthGoalServiceV0:

    def __init__(self):
        self.repo = HealthGoalRepository(db)

    def get_all_health_goals(self):
        return self.repo.get_all()

    def get_health_goal_by_id(self, health_goal_id: int):
        return self.repo.get_by_id(health_goal_id)

    def create_health_goal(self, name: str):
        new_id = len(self.repo.get_all()) + 1

        new_health_goal = HealthGoal(
            id=new_id,
            name=name
        )

        return self.repo.create(new_health_goal)

    def update_health_goal(self, health_goal_id: int, name: str):
        health_goal = self.repo.get_by_id(health_goal_id)

        if not health_goal:
            return None

        health_goal.name = name
        return health_goal

    def delete_health_goal(self, health_goal_id: int):
        health_goal = self.repo.get_by_id(health_goal_id)

        if not health_goal:
            return None

        self.repo.delete(health_goal_id)

        return {"message": "Health Goal deleted successfully"}
