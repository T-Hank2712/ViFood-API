from app.models.additive import Additive


class AdditiveRepository:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.additives

    def get_by_id(self, additive_id: int):
        return next((a for a in self.db.additives if a.id == additive_id), None)

    def create(self, additive: Additive):
        self.db.additives.append(additive)
        return additive

    def delete(self, additive_id: int):
        self.db.additives = [
            a for a in self.db.additives if a.id != additive_id
        ]
        return True
