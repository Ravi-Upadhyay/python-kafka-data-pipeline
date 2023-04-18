"""
MODULE: kafka_connector_service
Provide services and utilities for connecting with kafka
"""

from time import sleep
from kafka import KafkaProducer
import json

# Importing Constants
from constants import DEFAULT_ENCODING, FILE_LOCATION, KAFKA_HOST, KAFKA_TOPIC_INCOMING, SLEEP_TIME_BEFORE_READ_NEXT_LINE

# Kafka Producer
def get_kafka_producer(kafka_host = KAFKA_HOST, def_encoding = DEFAULT_ENCODING):
    """
    FUNCITON: get_kafka_producer(), generic function to return kafka host
    @returns: kafka producer using kafka-python library or Boolean(False) on failure
    @arguments: kafka_host, default_encoding used to write
    """
    try: 
        producer = KafkaProducer(bootstrap_servers=[kafka_host], value_serializer=lambda m: json.dumps(m).encode(def_encoding))
    except: 
        print('Error: get_kafka_producer()')
    finally: 
       return producer if get_kafka_producer_bootstrap_connected_status(producer) else False

def get_kafka_producer_bootstrap_connected_status(producer):
    """
    FUNCITON: get_kafka_producer_bootstrap_connected_status(), if connection to bootstrap is successful
    @returns: Boolean (True/False)
    @arguments: kafka_producer
    """
    return producer.bootstrap_connected()

def get_kafka_producer_metrics(producer):
    """
    FUNCITON: get_kafka_producer_metrics(), metrics of producer
    @returns: Metrics data
    @arguments: kafka_producer
    """
    return producer.metrics()