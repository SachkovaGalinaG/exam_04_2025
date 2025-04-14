FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
COPY app/ ./app/ 
COPY script.py . 
# CMD ["flask", "run", "-h", "0.0.0.0"]
