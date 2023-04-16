# Meetup RSVP data stream processing 

___

## Index

- App structure
- Instructions
- Reference from Web
- Todo List
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

- To install websocket flask
> [Flask Socket io](https://flask-socketio.readthedocs.io/en/latest/)
```python
$ pip3 install flask_socketio
```
> Web socket communication - Data transfer not working on Flask Server
> [Gunicorn](https://flask.palletsprojects.com/en/2.2.x/deploying/gunicorn/)
> gunicorn-20.1.0-py3-none-any.whl

```python
$ pip3 install gunicorn
```
> install eventlet
> dnspython-2.3.0 eventlet-0.33.3 greenlet-2.0.2 six-1.16.0
```python
$ pip3 install eventlet
```

> Another server, eventlet started but throwing some error. Trying this one
```python
pip3 install gevent
```

> Command to run gunicorn server
```python
gunicorn --worker-class eventlet -w 4 -b 127.0.0.1:5000 --log-level=debug app:app
# or
gunicorn --worker-class gevent -w 4 -b 127.0.0.1:5000 --log-level=debug app:app
# or
gunicorn -w 4 -b 127.0.0.1:5000 --log-level=debug app:app
# or 
gunicorn -w 4 -b 127.0.0.1:5000 app:app
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
$ bin/kafka-topics.sh --create --topic meetup-rsvp-true --bootstrap-server localhost:9092
```

> Topic created - meetup-rsvp

```bash

$ bin/kafka-topics.sh --describe --topic meetup-rsvp --bootstrap-server localhost:9092


```

2. <strong>Kafka client for Python</strong>
```python
pip install kafka-python
```

3. Additional dependencies

> [Flask Expects JSON](https://pypi.org/project/flask-expects-json/) Decorator for REST endpoints in flask. Validate JSON request data.
```python
$ pip3 install flask-expects-json
```

### Frontend

> [Library for socket implementation - socket.io client](https://socket.io/docs/v4/client-initialization/)

- Install socket client
```bash
npm i socket.io-client
```
- Install ImportMaps, as socket client import was not working
```bash
npm i --save-dev @web/dev-server-import-maps
```
___

## Reference From Web

___

## Todo List

[ ] Make backend service a single page application. [Flask Single Page App](https://flask.palletsprojects.com/en/2.2.x/patterns/singlepageapplications/)