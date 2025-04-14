from influxdb_client import InfluxDBClient

class InfluxDB:
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

influx = InfluxDB()