# Python slim = менший образ, швидший деплой
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Системні залежності, якщо треба psycopg/компіляція
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Нерутовий користувач
RUN useradd -m appuser
WORKDIR /app

# Виставимо залежності окремим шаром для кешу
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Скопіюємо код
COPY . .

# За потреби: змінити імпорт на твій модуль
# Припустимо, що в app.py є "app = Flask(__name__)"
EXPOSE 8080
USER appuser

# Gunicorn — продовий WSGI
CMD ["gunicorn", "-w", "2", "-k", "gthread", "-t", "60", "-b", "0.0.0.0:8080", "app:app"]
