"""
"""

from time import sleep
from kafka import KafkaConsumer, TopicPartition
import json

# Importing Constants
from constants import DEFAULT_ENCODING, FILE_LOCATION, KAFKA_HOST, KAFKA_TOPIC_INCOMING, KAFKA_TOPIC_OUTGOING, SLEEP_TIME_BEFORE_READ_NEXT_LINE

from kafka_connector_service import get_kafka_consumer

# Set up Kafka consumer
consumer = KafkaConsumer(bootstrap_servers=[KAFKA_HOST], value_deserializer=lambda m: json.loads(m.decode(DEFAULT_ENCODING)),  auto_offset_reset='earliest',  consumer_timeout_ms=2500, max_poll_records=10, group_id='common')

def data_pipeline_output_main(offset):

    topic_partition = TopicPartition(KAFKA_TOPIC_OUTGOING, 0)
    consumer.assign([topic_partition])

    consumer.seek(topic_partition, offset)
    events = consumer.poll(1000)
    # print('data_pipeline_output_main',events[topic_partition])

    return events[topic_partition]

if __name__ == '__main__':
    data_pipeline_output_main(start = 0)