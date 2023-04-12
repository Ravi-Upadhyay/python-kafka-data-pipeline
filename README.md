# Meetup RSVP data stream processing 

___

## Index

- App structure
- Instructions
___

## Folder Structurre

<pre>
|- requirement.md
|- sample.json
|- backendService (For now, backend code)
|-- app.py
</pre>

___

## Instructions

### Backend 

#### Installing Python

- To run the application

```python
# /backgroundService/
$ flask --app app run #to run app.py locally. 
```

- To install the Flask (Virtual environment)

```python
# /backgroundService/
$ python3 -m venv venv 
$ . venv/bin/activate

$ pip3 install Flask
```

#### Installing Apache Kafka

> Notes from the web:
>
> - [Kafka Intro](https://kafka.apache.org/intro)
> - [Kafka Quick Start Guide](https://kafka.apache.org/quickstart)

1. <strong>Kafka server</strong>

> Downloand Kafka from: [2.13-3.4.0](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.4.0/kafka_2.13-3.4.0.tgz)
```bash
$ cd kafka_2.13-3.4.0

# Start the ZooKeeper service
$ bin/zookeeper-server-start.sh config/zookeeper.properties

# Open another session and
# Start the Kafka broker service
$ bin/kafka-server-start.sh config/server.properties

# Start kafka topic
$ bin/kafka-topics.sh --create --topic meetup-rsvp --bootstrap-server localhost:9092
```

> Topic created - meetup-rsvp

```bash

$ bin/kafka-topics.sh --describe --topic meetup-rsvp --bootstrap-server localhost:9092

```

2. <strong>Kafka client for Python</strong>
```python
pip install kafka-python
```