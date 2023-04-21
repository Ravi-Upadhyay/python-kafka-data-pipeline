"""
MODULE: kafka_connector_service
Provide services and utilities for connecting with kafka
"""

from time import sleep
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json

# Importing Constants
from constants import DEFAULT_ENCODING, KAFKA_HOST, KAFKA_CONSUMER_TIMEOUT, KAFKA_CONSUMER_GROUP_ID, KAFKA_CONSUMER_MAX_POLL_RECORDS

# Kafka Producer
def get_kafka_producer(kafka_host, def_encoding = DEFAULT_ENCODING):
    """
    FUNCITON: get_kafka_producer(), generic function to return kafka host
    @returns: kafka producer using kafka-python library or Boolean(False) on failure
    @arguments: kafka_host, default_encoding(default = 'utf-8') used to write
    """
    try: 
        producer = KafkaProducer(bootstrap_servers=[kafka_host], value_serializer=lambda m: json.dumps(m).encode(def_encoding))
    except: 
        print('Error: get_kafka_producer()')
    finally: 
       return producer if get_kafka_bootstrap_connected_status(producer) else False
    
def produce_kafka_event(producer, kafka_topic, data):
    """
    FUNCITON: _produce_kafka_event_(), produce a rsvp event in kafka
    @returns: None
    @arguments: producer, kafka topic ,data for the event
    """
    try: 
        producer.send(kafka_topic, data)
    except: 
        print('Error: _produce_kafka_event_()')

def close_kafka_producer(producer):
    # Wait for any outstanding messages to be delivered and delivery reports received
    producer.flush()
    # Close the producer connection
    producer.close()

def get_kafka_bootstrap_connected_status(node):
    """
    FUNCITON: get_kafka_bootstrap_connected_status(), if connection to bootstrap is successful
    @returns: Boolean (True/False)
    @arguments: kafka_node
    """
    return node.bootstrap_connected()

def get_kafka_metrics(node):
    """
    FUNCITON: get_kafka_metrics(), metrics of producer
    @returns: Metrics data
    @arguments: kafka_node
    """
    return node.metrics()

# Kafka Consumer
def get_kafka_consumer_v2(kafka_topic, kafka_host, gi=KAFKA_CONSUMER_GROUP_ID, ctm=KAFKA_CONSUMER_TIMEOUT, aor='earliest'):
    try: 
        consumer = KafkaConsumer(bootstrap_servers=[kafka_host], group_id=gi, consumer_timeout_ms=ctm, auto_offset_reset=aor)
    except: 
        print('Error: get_kafka_consumer()')
    finally: 
       return consumer if get_kafka_bootstrap_connected_status(consumer) else False
    

def get_kafka_consumer(kafka_topic, kafka_host, aor = 'earliest'):
    """
    FUNCITON: get_kafka_consumer(), generic function to return kafka consumer
    @returns: kafka consumer using kafka-python library or Boolean(False) on failure
    @arguments: kafka_topic, kafka_host, auto_offset_reset(default = 'earliest')
    """
    try: 
        consumer = KafkaConsumer(kafka_topic, bootstrap_servers=[kafka_host], auto_offset_reset=aor)
    except: 
        print('Error: get_kafka_consumer()')
    finally: 
       return consumer if get_kafka_bootstrap_connected_status(consumer) else False

def close_kafka_consumer(consumer):
    # Unsubscribe from all partitions and topics
    consumer.unsubscribe()
    # Close the consumer connection
    consumer.close()

def kafka_seek_and_poll(consumer, topic_partition, offset = 0):
    consumer.seek(topic_partition, offset)
    polled_data = consumer.poll(1000, KAFKA_CONSUMER_MAX_POLL_RECORDS)
    return polled_data[topic_partition]    

def configure_kafka_consumer_topic_partition(consumer, kafka_topic, partition = 0):
    topic_partition = TopicPartition(kafka_topic, partition)
    consumer.assign([topic_partition])
    return topic_partition

def configure_kafka_consumer_subscribe(consumer, kafka_topic):
    consumer.subscribe(kafka_topic)