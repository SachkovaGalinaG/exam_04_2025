from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from app.models import Product
from app.extensions import mongo

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Получаем данные из формы
        name = request.form.get("name")
        current_sales = int(request.form.get("current_sales"))
        current_revenue = float(request.form.get("current_revenue"))
        category = request.form.get("category")

        # Проверка обязательных полей
        if not all([name, current_sales, current_revenue, category]):
            return "Missing required fields", 400

        # Создаем и сохраняем продукт с прогнозом
        product = Product(
            name=name,
            current_sales=current_sales,
            current_revenue=current_revenue,
            category=category
        )
        product.save()

        return redirect(url_for("main.index"))

    # Получаем все продукты с актуальными прогнозами
    products = Product.get_all()
    return render_template("index.html", 
                         products=products,
                         current_date=datetime.now().strftime("%Y-%m-%d"))

@main.route("/forecast")
def forecast():
    # Получаем агрегированные данные по прогнозам
    forecast_data = Product.get_sales_forecast()
    return render_template("forecast.html", 
                         forecast_data=forecast_data,
                         current_date=datetime.now().strftime("%Y-%m-%d"))

@main.route("/category/<category_name>")
def category_view(category_name):
    # Получаем прогнозы для конкретной категории
    products = Product.get_by_category(category_name)
    return render_template("category.html",
                         products=products,
                         category=category_name,
                         current_date=datetime.now().strftime("%Y-%m-%d"))

@main.route("/api/forecast")
def api_forecast():
    # JSON API для получения данных прогноза
    forecast_data = Product.get_sales_forecast()
    return jsonify(forecast_data)