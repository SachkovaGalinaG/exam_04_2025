from flask import Flask
from app.extensions import neo4j

def create_app():
    app = Flask(__name__)
    
    app.config.update(
        NEO4J_URI="bolt://neo4j:7687",
        NEO4J_USER="neo4j",
        NEO4J_PASSWORD="password123"
    )
    
    neo4j.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)

    return app