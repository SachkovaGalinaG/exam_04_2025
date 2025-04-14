from influxdb_client import InfluxDBClient
from datetime import datetime
import random

class VisitorForecast:
    def __init__(self, app=None):
        self.app = app
        self.client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.client = InfluxDBClient(
            url=app.config['INFLUXDB_URL'],
            token=app.config['INFLUXDB_TOKEN'],
            org=app.config['INFLUXDB_ORG']
        )

    def generate_forecast(self, location, current_visitors):
        forecast_data = {
            "location": location,
            "current": current_visitors,
            "forecast": round(current_visitors * random.uniform(1.1, 1.5)),
            "confidence": round(random.uniform(0.7, 0.95), 2),
            "timestamp": datetime.utcnow()
        }
        
        write_api = self.client.write_api()
        write_api.write(
            bucket=self.app.config['INFLUXDB_BUCKET'],
            record={
                "measurement": "visitor_forecasts",
                "tags": {"location": location},
                "fields": {
                    "current": current_visitors,
                    "forecast": forecast_data["forecast"],
                    "confidence": forecast_data["confidence"]
                },
                "time": forecast_data["timestamp"]
            }
        )
        return forecast_data