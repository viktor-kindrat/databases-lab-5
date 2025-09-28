FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-w", "2", "-k", "gthread", "-t", "60", "-b", "0.0.0.0:8080", "app:app"]
