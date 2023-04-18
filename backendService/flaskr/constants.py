"""
Module: constants.py
Declare constants for the project
"""

# File encoding
DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./../mocks/meetup.txt"

# While producing meetup rsvp events, sleep timer before producing events
SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2

# Kafka configurations
KAFKA_HOST = "localhost:9092"
KAFKA_TOPIC_INCOMING = "meetup-rsvp"
KAFKA_TOPIC_OUTGOING = "meetup-rsvp-true"
