FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir requests==2.32.5

COPY app.py .

CMD ["python", "-u", "app.py"]
