from datetime import datetime, timedelta
from .extensions import mongo

class Product:
    def __init__(self, name, current_sales, current_revenue, category):
        self.name = name
        self.current_sales = current_sales
        self.current_revenue = current_revenue
        self.category = category
        self.forecast = self._generate_forecast()

    def _generate_forecast(self):
        """Генерирует прогнозные данные на следующий квартал"""
        today = datetime.now()
        return {
            "next_quarter": {
                "projected_sales": int(self.current_sales * random.uniform(1.1, 1.5)),
                "projected_revenue": round(self.current_revenue * random.uniform(1.1, 1.8), 2),
                "confidence_level": round(random.uniform(0.7, 0.95), 2)
            },
            "forecast_date": today,
            "valid_until": today + timedelta(days=90)
        }

    def save(self):
        product_data = {
            "name": self.name,
            "current_sales": self.current_sales,
            "current_revenue": self.current_revenue,
            "category": self.category,
            "forecast": self.forecast,
            "last_updated": datetime.now()
        }
        return mongo.db.products.insert_one(product_data)

    @staticmethod
    def get_all():
        """Получение всех продуктов с актуальными прогнозами"""
        return list(mongo.db.products.find({
            "forecast.valid_until": {"$gt": datetime.now()}
        }))

    @staticmethod
    def get_by_category(category):
        """Получение прогнозов по категории"""
        return list(mongo.db.products.find({
            "category": category,
            "forecast.valid_until": {"$gt": datetime.now()}
        }))

    @staticmethod
    def get_sales_forecast():
        """Агрегация данных по прогнозам продаж"""
        pipeline = [
            {"$match": {"forecast.valid_until": {"$gt": datetime.now()}}},
            {"$group": {
                "_id": "$category",
                "total_projected_sales": {"$sum": "$forecast.next_quarter.projected_sales"},
                "total_projected_revenue": {"$sum": "$forecast.next_quarter.projected_revenue"},
                "avg_confidence": {"$avg": "$forecast.next_quarter.confidence_level"}
            }}
        ]
        return list(mongo.db.products.aggregate(pipeline))

    def __repr__(self):
        return f'<Product {self.name} (Category: {self.category})>'