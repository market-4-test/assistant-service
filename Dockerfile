# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY *.py ./

EXPOSE 8000

# Запускаем приложение из main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]