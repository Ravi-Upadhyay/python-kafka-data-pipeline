from time import sleep
from kafka import KafkaProducer, KafkaConsumer
import json

DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./streamMock/meetup.txt"
SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2
KAFKA_TOPIC_INCOMING = "meetup-rsvp"

# Note: Basic file open operation
# f = open(FILE_LOCATION, mode="rt", encoding=DEFAULT_ENCODING)
# line = f.readline()
# print(line)

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))

# Set up Kafka consumer
consumer = KafkaConsumer(KAFKA_TOPIC_INCOMING, bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')

for message in consumer:
    data = message.value.decode('utf-8')
    print(data)


# TODO: Cleaning based on anamolies found
def sanitizeInputBeforeEventCreation(d):
    return d


def processLine(l):
    sanitizedInput = sanitizeInputBeforeEventCreation(l)
    # print(sanitizedInput)

    producer.send(KAFKA_TOPIC_INCOMING, {'rsvp': sanitizedInput})
    sleep(SLEEP_TIME_BEFORE_READ_NEXT_LINE)


with open(FILE_LOCATION, mode="rt", encoding=DEFAULT_ENCODING) as openfileobject:
    for line in openfileobject:
        processLine(line)
    
    # Wait for any outstanding messages to be delivered and delivery reports received
    producer.flush()

    # Close the producer connection
    producer.close()

# def closeFileStream(f):
#     close(f)

