from flask import Flask
from app.extensions import mongo  # Импортируем MongoDB вместо SQLAlchemy
from app.routes import main

def create_app():
    app = Flask(__name__)
    
    # Загружаем конфигурацию
    app.config.from_prefixed_env()
    
    # Настройка подключения к MongoDB
    app.config["MONGO_URI"] = "mongodb://admin:admin@mongodb:27017/bilet12?authSource=admin"
    
    # Инициализируем MongoDB
    mongo.init_app(app)
    
    # Регистрируем blueprint
    app.register_blueprint(main)

    return app