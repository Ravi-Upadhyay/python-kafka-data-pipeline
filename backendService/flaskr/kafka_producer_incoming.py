"""
MODULE: kafka_producer_incoming:

1. It read data from a file (Contains sample data for Meetup's RSVP) line by line To simulate data stream
2. As Meetup's RSVP steaming API doesn't exist
3. It then produce those events in Kafka event bus

TODO: (Potential Microservice - 1): Indepedent script that can be migrated to the micro-service in future
"""

from time import sleep
from kafka import KafkaProducer
import json

# Importing Constants
from constants import DEFAULT_ENCODING, FILE_LOCATION, KAFKA_HOST, KAFKA_TOPIC_INCOMING, SLEEP_TIME_BEFORE_READ_NEXT_LINE

from kafka_connector_service import get_kafka_producer

def _get_kafka_producer_incoming_(kafka_host, def_encoding):
    """
    FUNCITON: _get_kafka_producer_incoming_(), get producer to produce incoming rsvp events
    @returns: A Kafka producer or Boolean (False)
    @arguments: kafka_host, def_encoding
    """
    producer = get_kafka_producer(kafka_host, def_encoding)
    return producer

def _produce_kafka_event_(producer, data):
    """
    FUNCITON: _produce_kafka_event_(), produce a rsvp event in kafka
    @returns: None
    @arguments: producer, data for the event
    """
    try: 
        producer.send(KAFKA_TOPIC_INCOMING, {'rsvp': data})
    except: 
        print('Error: _produce_kafka_event_()')

def _read_file_line_by_line_as_stream_(producer, file, def_encoding, sim_time):
    """
    FUNCITON: _read_file_line_by_line_as_stream_(), produce a rsvp event in kafka by reading line by line of the given file
    @returns: Number of records processed
    @arguments: producer, file location, encoding, simulation time(sleep)
    """
    count = 0
    try: 
        with open(file, mode="rt", encoding=def_encoding) as open_file_object:
            for line in open_file_object:
                _produce_kafka_event_(producer, line)
                sleep(sim_time)
                count += 1
    except: 
        print('Error: _read_file_line_by_line_as_stream_()')
    finally: 
        return count

def kafka_produce_incoming_main():
    """
    FUNCITON: kafka_produce_incoming_main(), main callable function of the module
    @returns: Number of records processed or Warning
    @arguments: None
    """
    producer = _get_kafka_producer_incoming_(KAFKA_HOST, DEFAULT_ENCODING)
    if producer != False:
        processed_records =_read_file_line_by_line_as_stream_(producer, FILE_LOCATION, DEFAULT_ENCODING, SLEEP_TIME_BEFORE_READ_NEXT_LINE)
        
        print('Info: kafka_produce_incoming_main(): records processed: ', processed_records)
        
        # Wait for any outstanding messages to be delivered and delivery reports received
        producer.flush()
        # Close the producer connection
        producer.close()
    else: 
        print('Warn: kafka_produce_incoming_main(), not able to get kafka producer.')

if __name__ == '__main__':
    kafka_produce_incoming_main()