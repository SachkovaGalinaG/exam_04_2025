from datetime import datetime
from app.extensions import neo4j

class HashtagAnalyzer:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def log_hashtags(self, post_id, hashtags):
        """Сохраняет хештеги в Neo4j и InfluxDB."""
        timestamp = datetime.utcnow()
        
        # Сохраняем в Neo4j
        for hashtag in hashtags:
            neo4j.add_hashtag(hashtag, post_id, timestamp)
        
    def get_trending_hashtags(self, hours=24, limit=10):
        """Возвращает популярные хештеги за последние N часов."""
        return neo4j.get_trending_hashtags(hours, limit)