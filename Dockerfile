FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Use gunicorn for production-style server
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
