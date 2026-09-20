FROM python:3.12-slim

WORKDIR /app

COPY python ./python

RUN pip install --no-cache-dir ./python

EXPOSE 8080

CMD ["python", "-m", "overflow.cli", "gateway", "--host", "0.0.0.0", "--port", "8080"]
