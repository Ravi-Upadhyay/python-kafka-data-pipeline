"""
MODULE: data_pipeline_processor:

1. It consumes data from the Kafka event queue
2. It validates the required data (Deal with data anamolies)
3. It processes the data based on requirements
4. It produces data to another pipeline

SAMPLE: validated data: 
{
    'venue': 
        {
            'venue_name': 'WeWork Hazerem', 
            'venue_id': 24951989, 
            'lon': 34.766663, 
            'lat': 32.050255
        }, 
    'response': True, 
    'rsvp_id': 1658878916}
    }
}

TODO: (Potential Microservice - 2): Indepedent script that can be migrated to the micro-service in future
"""
import json

# Importing Constants
from constants import DEFAULT_ENCODING, KAFKA_HOST, KAFKA_TOPIC_INCOMING, KAFKA_TOPIC_OUTGOING, KAFKA_DEFAULT_PARTITION

# Importing Modules
from kafka_connector_service import get_kafka_producer, get_kafka_consumer_v2, produce_kafka_event, configure_kafka_consumer_topic_partition, close_kafka_producer, close_kafka_consumer
from data_validation_filteration import filter_data_by_rsvp, validate_data_to_proceed

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
    consumer = get_kafka_consumer_v2(kafka_topic, kafka_host)
    return consumer

def consume_and_process_input(consumer, producer, kafka_topic_producer, def_encoding):
    """
    FUNCTION: consume_and_process_input(), Consume data from one event bus/queue/pipeline
    and process, validate, filter and Produce to final outgoing event bus/queue/pipeline
    @returns: Count of processed and finalEligible(filtered and validated) records
    @arguments: consumer (incoming pipeline), producer (outgoing pipeline), kafka topic (for producer), encoding
    """
    count_processed = 0
    count_rsvp_true = 0
    try: 
        for message in consumer:
            count_processed += 1
            data = json.loads(message.value.decode(def_encoding))
            # print('consume_and_process_input', data)
            if data is not None:
                validated_data = validate_data_to_proceed(data)
                # print('consume_and_process_input, validated data:', validated_data)

                filtered_rsvp = filter_data_by_rsvp(validated_data)

                if filtered_rsvp: 
                    count_rsvp_true += 1
                    produce_kafka_event(producer, kafka_topic_producer, validated_data)
    except ValueError:
        print('Error: consume_and_process_input(), ValueError, while reading from kafka incoming or Data Stream Ended')  
    finally: 
        return {'count_processed': count_processed, 'count_rsvp_true': count_rsvp_true}

def data_pipeline_processor_main():
    """
    FUNCTION: data_pipeline_processor_main(), main function of the module
    creates consumer(incoming), producer(outgoing) and calls function to process, validate, filter data
    @returns: None, initates connections to Kafka and closes them at the end. 
    @arguments: consumer (incoming pipeline), producer (outgoing pipeline), kafka topic (for producer), encoding
    """
    try: 
        consumer = _get_kafka_consumer_incoming_(KAFKA_TOPIC_INCOMING, KAFKA_HOST)
        producer = _get_kafka_producer_outgoing_(KAFKA_HOST, DEFAULT_ENCODING)

        if consumer != False and producer != False:
            topic_partition = configure_kafka_consumer_topic_partition(consumer, KAFKA_TOPIC_INCOMING, KAFKA_DEFAULT_PARTITION)
            consumed_and_processed_records = consume_and_process_input(consumer, producer, KAFKA_TOPIC_OUTGOING, DEFAULT_ENCODING)
        else: 
            print('Warn: data_pipeline_processor_main(), not able to get kafka producer or consumer.')
    except:
        print('Error: data_pipeline_processor_main()')
    finally: 
        print('Info: data_pipeline_processor_main(): records processed and people with RSVP(true) respectively: ', consumed_and_processed_records['count_processed'], consumed_and_processed_records['count_rsvp_true'])
        #Wait for any outstanding messages to be delivered and delivery reports received and close producer
        close_kafka_producer(producer)
        # Unsubscribe and close Consumer
        close_kafka_consumer(consumer)

if __name__ == '__main__':
    data_pipeline_processor_main()