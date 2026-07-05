from app.repositories.additive_repo import AdditiveRepository


class AdditiveServiceV1:

    def __init__(self, db):
        self.repo = AdditiveRepository(db)

    def get_all_additives(self):
        additives = self.repo.get_all()

        if not additives:
            raise ValueError("Additive Not Found")

        return additives

    def get_additive_by_id(self, additive_id: str):
        additive = self.repo.get_by_id(additive_id)

        if not additive:
            raise ValueError("Additive Not Found")

        return additive
