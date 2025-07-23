# coding: utf8

from confluent_kafka import Producer
from config import Config
import json


class KafkaProducer:
    def __init__(self, broker: str):
        self.producer = Producer({'bootstrap.servers': broker})

    def send(self, topic: str, key: str, value: dict):
        try:
            self.producer.produce(
                topic=topic,
                key=key,
                value=json.dumps(value),
            )
            self.producer.flush()
        except Exception as e:
            raise RuntimeError(f"Kafka produce failed: {e}")


kafka_producer = KafkaProducer(Config.KAFKA_BROKER)
