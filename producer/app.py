import time
import requests
import json
from kafka import KafkaProducer
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

KAFKA_BROKER = "redpanda:9092"
TOPIC_NAME = "btc-metrics"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_data():
    url = "http://btc-api:8000/btc-metrics"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error("Failed to fetch data from API: %s", e)  # Correct usage here
        return None

def produce():
    while True:
        data = fetch_data()
        logging.info("The fetching worked")  # Just a simple string
        if data:
            try:
                producer.send(TOPIC_NAME, value=data)
                producer.flush()
                logging.info(f"Sent to Kafka: {data}")  # Use %s formatting
            except Exception as e:
                logging.error("Failed to send to Kafka: %s", e)
        time.sleep(30)

if __name__ == "__main__":
    logging.info("Kafka Producer is running...")
    produce()
