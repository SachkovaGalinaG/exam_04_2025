import random
from datetime import datetime, timedelta
from app import create_app
from app.extensions import influx

app = create_app()

locations = [
    "Главный вход",
    "Выставочный зал", 
    "Кафе",
    "Конференц-зал",
    "Кинозал"
]

def generate_data():
    with app.app_context():
        # Явное создание и закрытие write_api
        write_api = influx.client.write_api()
        
        try:
            for day in range(30):
                timestamp = datetime.utcnow() - timedelta(days=30-day)
                records = []
                
                for location in locations:
                    current = random.randint(50, 200)
                    forecast = int(current * random.uniform(1.1, 1.5))
                    
                    records.append({
                        "measurement": "visitor_forecasts",
                        "tags": {"location": location},
                        "fields": {
                            "current": current,
                            "forecast": forecast,
                            "confidence": round(random.uniform(0.7, 0.95), 2)
                        },
                        "time": timestamp
                    })
                
                # Пакетная запись
                write_api.write(bucket="bilet15", record=records)
            
            print(f"Добавлены данные для {len(locations)} локаций за 30 дней")
        
        finally:
            # Обязательное закрытие API
            write_api.close()
            influx.client.close()

if __name__ == "__main__":
    generate_data()