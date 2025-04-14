# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

