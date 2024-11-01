import json
import logging
from aiokafka import AIOKafkaConsumer

from src.config import Settings

logging.basicConfig(level=logging.INFO)

def deserialize_message(message):
    try:
        message_str = message.decode('utf-8')
        return json.loads(message_str)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to deserialize message: {e}")
        return None

async def consume() -> None:
    consumer = AIOKafkaConsumer(
        Settings.PICTURE_TOPIC,
        bootstrap_servers=Settings.KAFKA_BOOTSTRAP_SERVERS,
    )
    await consumer.start()
    try:
        async for message in consumer:
            deserialized_message = deserialize_message(message.value)
            if deserialized_message:
                logging.info(deserialized_message)
    finally:
        await consumer.stop()