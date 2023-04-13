"""
MODULE: consumeKafkaStream:
1. It consumes data from the Kafka event queue
2. It validates the required data (Deal with data anamolies)
"""

from time import sleep
from kafka import KafkaConsumer
from flask_expects_json import expects_json
import json

DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./streamMock/meetup.txt"
SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2

KAFKA_HOST = "localhost:9092"
KAFKA_TOPIC_INCOMING = "meetup-rsvp"

# Set up Kafka consumer
consumer = KafkaConsumer(KAFKA_TOPIC_INCOMING, bootstrap_servers=[KAFKA_HOST], auto_offset_reset='earliest')

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



def consumeKafkaEvents(defEncoding):
    for message in consumer:
        try: 
            data = json.loads(message.value.decode(defEncoding))
            # print('Data from Kafka event bus: ', data)
            if data is not None:
                print(filterDataToProceed(data))
        except ValueError:
           pass
           

if __name__ == '__main__':
    consumeKafkaEvents(DEFAULT_ENCODING)