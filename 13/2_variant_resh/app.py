from flask import Flask, jsonify
from neo4j import GraphDatabase
import os 

app = Flask(__name__)

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

@app.route("/users")
def get_users():
    with driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u.name LIMIT 10")
        return jsonify([record["u.name"] for record in result])

@app.route("/hashtags/popular")
def popular_hashtags():
    with driver.session() as session:
        result = session.run("""
            MATCH (h:Hashtag)<-[:USES]-(p:Post)
            RETURN h.tag AS hashtag, COUNT(p) AS count
            ORDER BY count DESC
            LIMIT 10
        """)
        return jsonify([dict(record) for record in result])        

if __name__ == "__main__":
    app.run(host="0.0.0.0")