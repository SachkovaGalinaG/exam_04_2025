#!/bin/sh

# Ожидаем готовности InfluxDB
echo "Waiting for InfluxDB to be ready..."
while ! curl -s http://influxdb:8086/ping; do
  sleep 2
done

# Запускаем Flask приложение
echo "Starting Flask application..."
exec flask run --host=0.0.0.0 --port=5000