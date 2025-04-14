import random
from faker import Faker
from datetime import datetime, timedelta
from app.extensions import mongo  # Импортируем mongo из расширений
from app import create_app  # Импортируем создание приложения

fake = Faker()

categories = ['Electronics', 'Clothing', 'Home', 'Toys', 'Books', 'Food']

def generate_forecast_data():
    # Создаем Flask-приложение для доступа к конфигурации
    app = create_app()
    
    with app.app_context():  # Активируем контекст приложения
        today = datetime.now()
        next_quarter = today + timedelta(days=90)
        
        products = []
        for _ in range(100):
            category = random.choice(categories)
            product_data = {
                "name": fake.word().capitalize(),
                "current_sales": random.randint(1, 50),
                "current_revenue": round(random.uniform(100, 5000), 2),
                "category": category,
                "forecast": {
                    "next_quarter": {
                        "projected_sales": random.randint(10, 100),
                        "projected_revenue": round(random.uniform(500, 10000), 2),
                        "confidence_level": round(random.uniform(0.7, 0.95), 2)
                    },
                    "forecast_date": today,
                    "valid_until": next_quarter
                },
                "last_updated": today
            }
            products.append(product_data)
        
        # Вставка в MongoDB
        result = mongo.db.products.insert_many(products)
        print(f"Добавлено {len(result.inserted_ids)} прогнозов в MongoDB")

if __name__ == "__main__":
    generate_forecast_data()