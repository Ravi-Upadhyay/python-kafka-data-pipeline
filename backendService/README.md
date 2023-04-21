# Installation Instructions
___

### Backend application
#### Installation without docker

> If everything is installed. Backend service can be started via running backendService/flaskr/app.py

```bash
# Installing in virtual environment
# /backendService/
$ python3 -m venv venv 
$ . venv/bin/activate

$ pip install Flask[async]
$ pip install pytest coverage
$ pip install eventlet
$ pip install kafka-python
$ pip install flask-expects-json
```
___
### Apache Kafka

> Downloand Kafka from: [2.13-3.4.0](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.4.0/kafka_2.13-3.4.0.tgz)

```bash
$ cd kafka_2.13-3.4.0

# Start the ZooKeeper service
$ bin/zookeeper-server-start.sh config/zookeeper.properties

# Open another session and
# Start the Kafka broker service
$ bin/kafka-server-start.sh config/server.properties

# Start kafka topic (One time to create topics)
$ bin/kafka-topics.sh --create --topic meetup-rsvp --bootstrap-server localhost:9092
$ bin/kafka-topics.sh --create --topic meetup-rsvp-true --bootstrap-server localhost:9092

# Not necessary to see the status
$ bin/kafka-topics.sh --describe --topic meetup-rsvp --bootstrap-server localhost:9092
```

___
### Resources Over Web

> [Socket IO](https://socket.io/docs/v4/)

> [Flask Single Page App](https://flask.palletsprojects.com/en/2.2.x/patterns/singlepageapplications/)
___