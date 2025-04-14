from neo4j import GraphDatabase

class Neo4jDB:
    def __init__(self, app=None):
        self.app = app
        self.driver = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.driver = GraphDatabase.driver(
            app.config['NEO4J_URI'],
            auth=(app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD'])
        )
        # Создаем индекс при инициализации
        with self.get_session() as session:
            session.run("CREATE INDEX ON :Hashtag(name)")

    def get_session(self):
        return self.driver.session()

    def add_hashtags(self, post_id, hashtags):
        with self.get_session() as session:
            for hashtag in hashtags:
                session.run(
                    """
                    MERGE (h:Hashtag {name: $hashtag})
                    ON CREATE SET h.usage_count = 1
                    ON MATCH SET h.usage_count = h.usage_count + 1
                    MERGE (p:Post {id: $post_id})
                    CREATE (p)-[:TAGGED_WITH {timestamp: datetime()}]->(h)
                    """,
                    hashtag=hashtag.lower(),
                    post_id=post_id
                )

    def get_trending_hashtags(self, hours=24, limit=10):
        with self.get_session() as session:
            result = session.run(
                """
                MATCH (h:Hashtag)<-[r:TAGGED_WITH]-(p:Post)
                WHERE r.timestamp > datetime() - duration('PT%dH')
                RETURN h.name AS hashtag, h.usage_count AS total_count, COUNT(r) AS recent_count
                ORDER BY recent_count DESC, total_count DESC
                LIMIT $limit
                """ % hours,
                limit=limit
            )
            return [{
                "hashtag": record["hashtag"],
                "total_uses": record["total_count"],
                "recent_uses": record["recent_count"]
            } for record in result]

neo4j = Neo4jDB()