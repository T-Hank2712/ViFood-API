from app.models.health_goal import HealthGoal

health_goals = [
    HealthGoal(id=1, name="Giảm cân"),
    HealthGoal(id=2, name="Tăng cơ"),
    HealthGoal(id=3, name="Duy trì sức khỏe")]


class HealthGoalServiceV0:

    @staticmethod
    def get_all_health_goals(): return health_goals

    @staticmethod
    def get_health_goal_by_id(health_goal_id: int):
        return next((h for h in health_goals if h.id == health_goal_id), None)
    
    @staticmethod
    def create_health_goal(name: str):
        new_id = max(h.id for h in health_goals) + 1 if health_goals else 1
        new_health_goal = HealthGoal(id=new_id, name=name)
        health_goals.append(new_health_goal)
        return new_health_goal
    
    @staticmethod
    def update_health_goal(health_goal_id: int, name: str):
        health_goal = HealthGoalServiceV0.get_by_id(health_goal_id)
        if health_goal:
            health_goal.name = name
            return health_goal
        return None
    
    @staticmethod
    def delete_health_goal(health_goal_id: int):
        global health_goals
        health_goals = [h for h in health_goals if h.id != health_goal_id]
        return {"message": "Health Goal deleted successfully"}
