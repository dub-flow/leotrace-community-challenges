FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir Flask==3.0.0

COPY app.py .

EXPOSE 5000

CMD ["python3", "app.py"]
