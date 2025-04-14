from flask import Blueprint, render_template, request, current_app
from datetime import datetime
from app.extensions import influx

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location = request.form.get("location")
        current = request.form.get("current_visitors")
        
        if not all([location, current]):
            current_app.logger.error("Missing required fields")
            return render_template("index.html", forecasts=[], error="Не заполнены обязательные поля")
        
        try:
            write_api = influx.client.write_api()
            write_api.write(
                bucket="bilet15",
                record={
                    "measurement": "visitor_forecasts",
                    "tags": {"location": location},
                    "fields": {
                        "current": int(current),
                        "forecast": int(int(current) * 1.3),
                        "confidence": 0.85
                    },
                    "time": datetime.utcnow()
                }
            )
        except Exception as e:
            current_app.logger.error(f"Write error: {str(e)}")
            return render_template("index.html", forecasts=[], error="Ошибка сохранения данных")

    try:
        query_api = influx.client.query_api()
        query = '''
        from(bucket: "bilet15")
          |> range(start: -7d)
          |> filter(fn: (r) => r._measurement == "visitor_forecasts")
          |> pivot(rowKey: ["_time", "location"], columnKey: ["_field"], valueColumn: "_value")
          |> group(columns: ["location"])
          |> sort(columns: ["_time"], desc: true)
          |> limit(n: 1)
        '''
        result = query_api.query(query)
        
        forecasts = []
        for table in result:
            for record in table.records:
                forecasts.append({
                    "location": record.values.get("location"),
                    "current": record.values.get("current"),
                    "forecast": record.values.get("forecast"),
                    "confidence": record.values.get("confidence"),
                    "time": record.get_time()
                })
        
        return render_template("index.html", forecasts=forecasts)
    
    except Exception as e:
        current_app.logger.error(f"Query error: {str(e)}")
        return render_template("index.html", forecasts=[], error="Ошибка загрузки данных")

    try:
        query_api = influx.client.query_api()
        query = '''
        from(bucket: "bilet15")
          |> range(start: -7d)
          |> filter(fn: (r) => r._measurement == "visitor_forecasts")
          |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> group(columns: ["location"])
          |> last()
        '''
        result = query_api.query(query)
        
        forecasts = []
        for table in result:
            for record in table.records:
                forecasts.append({
                    "location": record.values.get("location"),
                    "current": record.values.get("current"),
                    "forecast": record.values.get("forecast"),
                    "confidence": record.values.get("confidence"),
                    "time": record.get_time()
                })
        
        return render_template("index.html", forecasts=forecasts)
    
    except Exception as e:
        current_app.logger.error(f"Query error: {str(e)}")
        return render_template("index.html", forecasts=[], error="Ошибка загрузки данных")