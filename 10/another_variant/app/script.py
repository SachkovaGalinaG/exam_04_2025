from faker import Faker
import random
 
from app import create_app
from app.extensions import db
from app.models import Product
 
app = create_app()
 
# 
def seed_database():
    fake = Faker()
    categories = ['Electronics', 'Clothing', 'Home', 'Toys', 'Books', 'Food']
 
    try:
        db.create_all()
        Product.query.delete()
 
        products = [
            Product(
                name=f"{fake.word().capitalize()} {fake.word()}",
                quantity_sold=random.randint(1, 100),
                total_revenue=round(random.uniform(10, 1000), 2),
                category=random.choice(categories)
            )
            for _ in range(100)
        ]
 
        db.session.bulk_save_objects(products)
        db.session.commit()
        print(f"✅ Успешно добавлено {len(products)} товаров.")
 
    except Exception as e:
        db.session.rollback()
        print(f"❌ Ошибка при заполнении БД: {str(e)}")
        raise
 
if __name__ == '__main__':
    with app.app_context():  
        seed_database()