"""
MODULE: consumeKafkaStream:
1. It consumes data from the Kafka event queue
2. It validates the required data (Deal with data anamolies)
"""

from time import sleep
from kafka import KafkaConsumer, KafkaProducer
import json
from constants import DEFAULT_ENCODING, FILE_LOCATION, KAFKA_HOST, KAFKA_TOPIC_OUTGOING, KAFKA_TOPIC_INCOMING, SLEEP_TIME_BEFORE_READ_NEXT_LINE
# DEFAULT_ENCODING = "utf-8"
# FILE_LOCATION = "./../mocks/meetup.txt"
# SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2

# KAFKA_HOST = "localhost:9092"
# KAFKA_TOPIC_INCOMING = "meetup-rsvp"
# KAFKA_TOPIC_OUTGOING = "meetup-rsvp-true"

# Set up Kafka consumer
consumer = KafkaConsumer(KAFKA_TOPIC_INCOMING, bootstrap_servers=[KAFKA_HOST], auto_offset_reset='earliest')

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers=[KAFKA_HOST], value_serializer=lambda m: json.dumps(m).encode(DEFAULT_ENCODING))

def filterDataVenue(d):
    # print('from filterDataVenue: ', d)
    venue_name = d['venue_name'] if 'venue_name' in d else None
    venue_id = d['venue_id'] if 'venue_id' in d else None
    lon = d['lon'] if 'lon' in d else None
    lat = d['lat'] if 'lat' in d else None

    if lon is not None and lat is not None:
        return {'venue_name': venue_name, 'venue_id': venue_id, 'lon': lon, 'lat':lat}
    return None

def filterDataResponse(d):
    return True if d == 'yes' else False

def filterDataRsvp(d):
    # print('From filterDataRsvp: ', d)
    venue = filterDataVenue(d['venue']) if 'venue' in d else None
    response = filterDataResponse(d['response']) if 'response' in d else None
    rsvp_id = d['rsvp_id'] if 'rsvp_id' in d else None

    if venue is not None and response is not None:
        return {'venue': venue, 'response': response, 'rsvp_id': rsvp_id}
    return None

def filterDataToProceed(d): 
    # print('From filterDataToProceed: ', d)
    if 'rsvp' in d and d['rsvp'] is not None:
        return filterDataRsvp(json.loads(d['rsvp']))
    return None



def consumeKafkaEvents(defEncoding = DEFAULT_ENCODING):
    for message in consumer:
        try: 
            data = json.loads(message.value.decode(defEncoding))
            # print('Data from Kafka event bus: ', data)
            if data is not None:
                filterdData = filterDataToProceed(data)
                # print(filterdData)
                if filterdData is not None and filterdData['response'] == True:
                    print(filterdData)
                    producer.send(KAFKA_TOPIC_OUTGOING, filterdData)

        except ValueError:
           pass   

if __name__ == '__main__':
    consumeKafkaEvents()