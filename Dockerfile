FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY distributed-redis.py .

CMD ["fastapi", "dev", "distributed-redis.py", "--host", "0.0.0.0"]