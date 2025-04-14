import random
from datetime import datetime, timedelta
from neo4j import GraphDatabase

URI = "bolt://neo4j:7687"
USER = "neo4j"
PASSWORD = "password123"

HASHTAGS = ["python", "data", "neo4j", "docker", "flask", "ai", "ml", "devops"]

def generate_test_data():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # Очистка данных
            session.run("MATCH (n) DETACH DELETE n")
            
            # Создание 1000 постов с хэштегами
            for i in range(1, 1001):
                post_id = f"post_{i}"
                tags = random.sample(HASHTAGS, random.randint(1, 4))
                
                for tag in tags:
                    session.run(
                        """
                        MERGE (h:Hashtag {name: $tag})
                        ON CREATE SET h.usage_count = 1
                        ON MATCH SET h.usage_count = h.usage_count + 1
                        MERGE (p:Post {id: $post_id})
                        CREATE (p)-[:TAGGED_WITH {
                            timestamp: $time
                        }]->(h)
                        """,
                        tag=tag.lower(),
                        post_id=post_id,
                        time=(datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
                    )
            
            print(f"Сгенерировано 1000 постов с хэштегами. Статистика:")
            
            # Получаем топ-5 хэштегов
            result = session.run(
                """
                MATCH (h:Hashtag)
                RETURN h.name AS name, h.usage_count AS count
                ORDER BY count DESC
                LIMIT 5
                """
            )
            
            for record in result:
                print(f"{record['name']}: {record['count']} использований")
    
    finally:
        driver.close()

if __name__ == "__main__":
    generate_test_data()