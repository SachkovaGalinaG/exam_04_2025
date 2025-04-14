FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Добавляем скрипт запуска
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

CMD ["/startup.sh"]