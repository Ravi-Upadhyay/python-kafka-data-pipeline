"""
MODULE: constants.py
Declare constants for the project
"""

# File encoding
DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./../mocks/meetup.txt"

# While producing meetup rsvp events, sleep timer before producing events
SLEEP_TIME_BEFORE_READ_NEXT_LINE = 1

# Kafka configurations
KAFKA_HOST = "localhost:9092"
KAFKA_TOPIC_INCOMING = "meetup-rsvp"
KAFKA_TOPIC_OUTGOING = "meetup-rsvp-true"
KAFKA_CONSUMER_TIMEOUT = 2000
KAFKA_CONSUMER_MAX_POLL_RECORDS = 10
KAFKA_CONSUMER_GROUP_ID = 'common'
KAFKA_DEFAULT_PARTITION = 0
KAFKA_DEFAULT_OFFSET = 0
