"""
MODULE: consumeKafkaStream:
1. It consumes data from the Kafka event queue
"""

from time import sleep
from kafka import KafkaConsumer
import json

DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./streamMock/meetup.txt"
SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2

KAFKA_HOST = "localhost:9092"
KAFKA_TOPIC_INCOMING = "meetup-rsvp"

# Set up Kafka consumer
consumer = KafkaConsumer(KAFKA_TOPIC_INCOMING, bootstrap_servers=[KAFKA_HOST], auto_offset_reset='earliest')

# TODO: Cleaning based on anamolies found
def sanitizeDataBeforeProcessing(d):
    return d

def processDataFromKafka(d): 
    return d

def consumeKafkaEvents(defEncoding):
    for message in consumer:
        data = message.value.decode(defEncoding)
        print('Data from Kafka event bus: ', data)

if __name__ == '__main__':
    consumeKafkaEvents(DEFAULT_ENCODING)