FROM python:3.7-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY application.py .
COPY config.py .
COPY models.py .
COPY schemas ./schemas
COPY controllers ./controllers

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "application", "--bind=0.0.0.0:8080", "--reload"]
