from neo4j import GraphDatabase
from dotenv import load_dotenv
from app.core.config import settings

load_dotenv()


class Neo4jConnection:
    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def get_driver(self):
        return self.driver

    def close(self):
        self.driver.close()

    def get_session(self):
        return self.driver.session()


neo4j_db = Neo4jConnection(
    uri=settings.neo4j_uri,
    username=settings.neo4j_username,
    password=settings.neo4j_password,
    database=settings.neo4j_database,
)

kc_db = Neo4jConnection(
    uri=settings.kc_neo4j_uri,
    username=settings.kc_neo4j_username,
    password=settings.kc_neo4j_password,
    database=settings.kc_neo4j_database,
)
