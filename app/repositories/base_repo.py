from app.helpers.id_generator import generate_id
from app.helpers.convert_time import now_iso


class BaseRepository:
    def __init__(self, db):
        self.driver = db.driver
        self.database = db.database

    def write(self, tx_func):
        with self.driver.session(database=self.database) as session:
            return session.execute_write(tx_func)

    def read(self, tx_func):
        with self.driver.session(database=self.database) as session:
            return session.execute_read(tx_func)

    def prepare_entity(self, data: dict) -> dict:
        data = dict(data)

        if not data.get("id"):
            data["id"] = generate_id()

        data.setdefault("createdAt", now_iso())
        data["updatedAt"] = now_iso()

        return data
    
    def prepare_update_entity(self, data: dict) -> dict:
        data = dict(data)
        data["updatedAt"] = now_iso()
        return data
