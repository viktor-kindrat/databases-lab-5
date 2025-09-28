FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# якщо у тебе є requirements.txt — залишаємо кешування
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# код
COPY . /app

# прод-режим і порт для waitress (твій app.py їх читає)
ENV FLASK_ENV=production APP_PORT=8080
EXPOSE 8080

# стартуємо прямо твій app.py
CMD ["python", "app.py"]
