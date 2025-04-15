from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Product

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            name = request.form.get('name')
            quantity_sold = int(request.form.get('quantity_sold', 0))
            total_revenue = float(request.form.get('total_revenue', 0))
            category = request.form.get('category')
            
            # Валидация данных
            if not all([name, category]) or quantity_sold <= 0 or total_revenue <= 0:
                flash('Invalid input data', 'error')
                return redirect(url_for('main.index'))
            
            # Создание и сохранение продукта
            product = Product(
                name=name,
                quantity_sold=quantity_sold,
                total_revenue=total_revenue,
                category=category
            )
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('main.index'))
    
    # GET-запрос - отображаем список продуктов
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('index.html', products=products)