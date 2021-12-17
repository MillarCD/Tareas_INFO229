FROM python:3.8-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3

RUN pip install pika
RUN pip install requests 
RUN pip install -U python-dotenv 

ENV PYTHONUNBUFFERED 1

COPY . componente_clima/

CMD ["python", "componente_clima/clima_manager.py"]
