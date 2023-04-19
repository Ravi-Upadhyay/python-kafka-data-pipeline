"""
MODULE: data_pipeline_processor:

1. It consumes data from the Kafka event queue
2. It validates the required data (Deal with data anamolies)
3. It processes the data based on requirements
4. It produces data to another pipeline

TODO: (Potential Microservice - 2): Indepedent script that can be migrated to the micro-service in future
"""

from time import sleep
from kafka import KafkaConsumer, KafkaProducer
import json

# Importing Constants
from constants import DEFAULT_ENCODING, FILE_LOCATION, KAFKA_HOST, KAFKA_TOPIC_INCOMING, KAFKA_TOPIC_OUTGOING, SLEEP_TIME_BEFORE_READ_NEXT_LINE

from kafka_connector_service import get_kafka_producer, get_kafka_consumer, produce_kafka_event

def _get_kafka_producer_outgoing_(kafka_host, def_encoding):
    """
    FUNCITON: _get_kafka_producer_outgoing_(), get producer to produce processed rsvp event
    @returns: A Kafka producer or Boolean (False)
    @arguments: kafka_host, def_encoding
    """
    producer = get_kafka_producer(kafka_host, def_encoding)
    return producer

def _get_kafka_consumer_incoming_(kafka_topic, kafka_host):
    """
    FUNCITON: _get_kafka_consumer_incoming_(), get consumer to consume incoming rsvp events
    @returns: A Kafka consumer or Boolean (False)
    @arguments: kafka_topic, kafka_host
    """
    consumer = get_kafka_consumer(kafka_topic, kafka_host)
    return consumer


def data_validate_venue(d):
    print('from data_validate_venue: ', d)
    venue_name = d['venue_name'] if 'venue_name' in d else None
    venue_id = d['venue_id'] if 'venue_id' in d else None
    lon = d['lon'] if 'lon' in d else None
    lat = d['lat'] if 'lat' in d else None

    if lon is not None and lat is not None:
        return {'venue_name': venue_name, 'venue_id': venue_id, 'lon': lon, 'lat':lat}
    return None

def data_validate_response(d):
    return True if d == 'yes' else False

def data_validate_and_filter_rsvp(d):
    print('From data_validate_and_filter_rsvp: ', d)
    
    venue = data_validate_venue(d['venue']) if 'venue' in d else None
    response = data_validate_response(d['response']) if 'response' in d else None
    rsvp_id = d['rsvp_id'] if 'rsvp_id' in d else None

    if venue is not None and response is not None:
        return {'lon': venue['lon'], 'lat': venue['lat'], 'response': response, 'rsvp_id': rsvp_id}
    return None
    

def validate_data_to_proceed(d): 
    print('From validate_data_to_proceed: ', d)

    if 'rsvp' in d and d['rsvp'] is not None:
        return data_validate_and_filter_rsvp(json.loads(d['rsvp']))
    return None

def check_rsvp_status(data):
    return data is not None and data['response'] == True

def consume_and_process_input(consumer, producer, kafka_topic_producer, def_encoding):
    count_processed = 0
    count_rsvp_true = 0
    for message in consumer:
        try: 
            count_processed += 1
            data = json.loads(message.value.decode(def_encoding))
            
            if data is not None:
                validated_data = validate_data_to_proceed(data)

                if validated_data is not None and validated_data['response'] == True:
                    count_rsvp_true += 1
                    print(validated_data)
                    produce_kafka_event(producer, kafka_topic_producer, validated_data)

            # validated_data = validate_data_to_proceed(data)
            # rsvp_status = check_rsvp_status(validated_data)
            
            # count_processed += 1

            # if rsvp_status:
            #     produce_kafka_event(producer, kafka_topic_producer, validated_data)
            #     count_rsvp_true += 1

        except ValueError:
            print('Error: consume_and_process_input(), ValueError, while reading from kafka incoming')  
        except: 
            print('Error: consume_and_process_input()')
        finally: 
            return {'count_processed': count_processed, 'count_rsvp_true': count_rsvp_true}

def data_pipeline_processor_main():
    consumer = _get_kafka_consumer_incoming_(KAFKA_TOPIC_INCOMING, KAFKA_HOST)
    producer = _get_kafka_producer_outgoing_(KAFKA_HOST, DEFAULT_ENCODING)

    if consumer != False and producer != False:
        consumed_and_processed_records = consume_and_process_input(consumer, producer, KAFKA_TOPIC_OUTGOING, DEFAULT_ENCODING)

        print('Info: data_pipeline_processor_main(): records processed and people with RSVP(true) respectively: ', consumed_and_processed_records['count_processed'], consumed_and_processed_records['count_rsvp_true'])

        # Wait for any outstanding messages to be delivered and delivery reports received
        # producer.flush()
        # Close the producer connection
        # producer.close()

        # Unsubscribe Consumer
        # consumer.unsubscribe()
    else: 
        print('Warn: data_pipeline_processor_main(), not able to get kafka producer or consumer.')

if __name__ == '__main__':
    data_pipeline_processor_main()