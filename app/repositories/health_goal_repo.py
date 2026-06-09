from app.models.health_goal import HealthGoal


class HealthGoalRepository:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.health_goals

    def get_by_id(self, health_goal_id: int):
        return next((h for h in self.db.health_goals if h.id == health_goal_id), None)

    def create(self, health_goal: HealthGoal):
        self.db.health_goals.append(health_goal)
        return health_goal

    def delete(self, health_goal_id: int):
        self.db.health_goals[:] = [h for h in self.db.health_goals if h.id != health_goal_id]
        return True
