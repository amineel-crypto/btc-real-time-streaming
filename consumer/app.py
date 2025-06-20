from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

logging.info("Starting the consumer...")

KAFKA_BROKER = "redpanda:9092"
TOPIC_NAME = "btc-metrics"

# MongoDB setup
MONGO_HOST = "mongodb"
MONGO_PORT = 27017
DB_NAME = "btc_db"
COLLECTION_NAME = "metrics"

# Connect to MongoDB
mongo_client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Kafka consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="btc-metrics-consumer-group",
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    max_poll_interval_ms=300000,  # 5 minutes, adjust if needed
    max_poll_records=10  # smaller batch size for faster processing
)

logging.info("Consumer is running and saving to MongoDB...")

try:
    for message in consumer:
        data = message.value
        logging.info(f"Received: {data}")
        try:
            collection.insert_one(data)
            logging.info("Saved to MongoDB")
        except Exception as e:
            logging.error(f"Failed to save data: {e}")
except KeyboardInterrupt:
    logging.info("Consumer stopped by user")
except Exception as e:
    logging.error(f"Unexpected error in consumer: {e}")
