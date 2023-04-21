"""
MODULE: data_pipeline_output:

1. It reads/conumes data from Kafka event bus which has processed data
2. Everytime this module is called. It processes some records to give to the front end over a web socket connection

TODO: (Potential Microservice (With Main App))
"""
# Importing Constants
from constants import DEFAULT_ENCODING, FILE_LOCATION, KAFKA_HOST, KAFKA_TOPIC_INCOMING, KAFKA_TOPIC_OUTGOING, SLEEP_TIME_BEFORE_READ_NEXT_LINE, KAFKA_DEFAULT_PARTITION, KAFKA_DEFAULT_OFFSET

# Importing Modules
from kafka_connector_service import get_kafka_consumer_v2, configure_kafka_consumer_topic_partition, kafka_seek_and_poll, close_kafka_consumer

def _get_kafka_consumer_outgoing_(kafka_topic, kafka_host):
    """
    FUNCITON: _get_kafka_consumer_outgoing_(), get consumer to consume outgoing or processed rsvp events
    @returns: A Kafka consumer or Boolean (False)
    @arguments: kafka_topic, kafka_host
    """
    consumer = get_kafka_consumer_v2(kafka_topic, kafka_host)
    return consumer

def data_pipeline_output_main(offset = KAFKA_DEFAULT_OFFSET): 
    """
    FUNCITON: data_pipeline_output_main(), main callable function of the module
    @returns: List of events (Meet Up Rsvp True) or None
    @arguments: offset
    """
    try:
        consumer = _get_kafka_consumer_outgoing_(KAFKA_TOPIC_OUTGOING,KAFKA_HOST)
        if consumer != False:
            topic_partition = configure_kafka_consumer_topic_partition(consumer, KAFKA_TOPIC_OUTGOING, KAFKA_DEFAULT_PARTITION)
            events = kafka_seek_and_poll(consumer, topic_partition, offset)
        else: 
            print('Warn: data_pipeline_output_main(), not able to get kafka producer or consumer.')
    except:
        print('Error: data_pipeline_output_main(), ')
    finally: 
        events_count = len(events) if events is not None else 0
        print('Info: data_pipeline_output_main(), events produced: ',str(events_count))
        close_kafka_consumer(consumer)
        return events if events_count > 0 else None

if __name__ == '__main__':
    data_pipeline_output_main()