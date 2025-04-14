FROM python:3.11-slim

# Устанавливаем системные зависимости для работы с mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект в контейнер
COPY . /app/

# Запускаем Gunicorn для работы с Django
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
