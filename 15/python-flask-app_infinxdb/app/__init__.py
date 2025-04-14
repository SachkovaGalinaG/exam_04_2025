from flask import Flask
from app.extensions import influx

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config.update(
        INFLUXDB_URL="http://influxdb:8086",
        INFLUXDB_TOKEN="my-admin-token",
        INFLUXDB_ORG="my-org",
        INFLUXDB_BUCKET="bilet15"
    )
    
    # Инициализация расширений
    influx.init_app(app)
    
    # Регистрация blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app