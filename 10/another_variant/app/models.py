from .extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_revenue = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    
def __repr__(self):
        return f'<Product {self.name}>'