FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 📌 ЭНЭ ХЭСГИЙГ ЗААВАЛ НЭМ
RUN pip install opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-flask

COPY . .

CMD ["python", "app.py"]
