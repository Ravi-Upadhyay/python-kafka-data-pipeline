"""
MODULE: kafka_connector_service
Provide services and utilities for connecting with kafka
"""

from time import sleep
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json

# Importing Constants
from constants import DEFAULT_ENCODING, KAFKA_HOST

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
    

def get_kafka_consumer_topic_partition(kafka_topic, partition):
    return  TopicPartition(kafka_topic, partition)
