# coding: utf8

import os

DEFAULT_PAGE_LIMIT = 50
DEFAULT_PAGE_NUMBER = 1
TIMEOUT_VALUE = 30

KAFKA_BOOKING_TOPIC = os.environ.get("KAFKA_BOOKING_TOPIC", "<your-kafka-booking-topic>")