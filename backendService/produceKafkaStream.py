"""
MODULE: produceKafkaStream:
1. It read data from a file (Contains sample data for Meetup's RSVP) line by line To simulate data stream
2. As Meetup's RSVP steaming API doesn't exist
3. It then produce those events in Kafka event bus
"""

from time import sleep
from kafka import KafkaProducer
import json

DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./streamMock/meetup.txt"
SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2

KAFKA_HOST = "localhost:9092"
KAFKA_TOPIC_INCOMING = "meetup-rsvp"

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers=[KAFKA_HOST], value_serializer=lambda m: json.dumps(m).encode(DEFAULT_ENCODING))

# Set up Kafka consumer
# consumer = KafkaConsumer(KAFKA_TOPIC_INCOMING, bootstrap_servers=[KAFKA_HOST], auto_offset_reset='earliest')

# for message in consumer:
#     data = message.value.decode('utf-8')
#     print(data)

# def consumeKafka():
#     for message in consumer:
#         data = message.value.decode(DEFAULT_ENCODING)
#         print('Reading from kafka pipeline: ', data)

# TODO: Cleaning based on anamolies found
def sanitizeInputBeforeEventCreation(d):
    return d

def produceKafkaEvent(data):
    sanitizedInput = sanitizeInputBeforeEventCreation(data)
    print('Reading from file: ', sanitizedInput)
    producer.send(KAFKA_TOPIC_INCOMING, {'rsvp': sanitizedInput})

def readFileLineByLineAsStream(file, defEncoding, simTime):
    with open(file, mode="rt", encoding=defEncoding) as openfileobject:
        for line in openfileobject:
            produceKafkaEvent(line)
            sleep(simTime)

# with open(FILE_LOCATION, mode="rt", encoding=DEFAULT_ENCODING) as openfileobject:
#     for line in openfileobject:
#         processLine(line)
    
    # Wait for any outstanding messages to be delivered and delivery reports received
    # producer.flush()

    # Close the producer connection
    # producer.close()

# def closeFileStream(f):
#     close(f)

# consumeKafka()

if __name__ == '__main__':
    readFileLineByLineAsStream(FILE_LOCATION, DEFAULT_ENCODING, SLEEP_TIME_BEFORE_READ_NEXT_LINE)