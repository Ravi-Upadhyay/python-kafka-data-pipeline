"""
Module: Main/Root Application
This is a single page application
Communicates with the front end over web socket
"""

from flask import Flask, jsonify, redirect
from kafka import KafkaConsumer
from flask_socketio import SocketIO, emit, send
import json
import eventlet
import asyncio
from asgiref.wsgi import WsgiToAsgi

DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./streamMock/meetup.txt"
SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2

KAFKA_HOST = "localhost:9092"
KAFKA_TOPIC_INCOMING = "meetup-rsvp"
KAFKA_TOPIC_OUTGOING = "meetup-rsvp-true"

app = Flask(__name__, static_folder='app', static_url_path="/app")

# Initialize Socket - Kept commented debug mode initialization
# socketio = SocketIO(app, cors_allowed_origins='*')
socketio = SocketIO(app, cors_allowed_origins='*', logger=True, engineio_logger=True)

# Set up Kafka consumer
consumer = KafkaConsumer(KAFKA_TOPIC_OUTGOING, bootstrap_servers=[KAFKA_HOST], auto_offset_reset='earliest')

def simulateRsvpMessage(offset):
    start = int(offset)
    end = start + 5
    messageList = []

    for x in range(start, end):
        message = { 'offsetCount': x }
        messageList.append(message)
    
    return { 'messageList': messageList, 'end': end }

def getRsvpFromKafkaConsumer(offset):
    counter = 0
    start = int(offset)
    end = 0
    messageList = []
    
    for message in consumer: 
        kafka_offset = int(message.offset)
        if kafka_offset > start and counter <= 4:
            counter += 1
            data = json.loads(message.value.decode(DEFAULT_ENCODING))
            finalMessage = { 'rsvp_id': str(data['rsvp_id']) }
            # print('dataFrom getRsvpFromKafkaConsumer: ', finalMessage)
            messageList.append(finalMessage)

    return { 'messageList': messageList, 'end': end }

# ----------------------- HTTP Communication ---------------------------

# Keepalive endpoint for monitorint the health
@app.route("/keepalive")
def keepalive():
    return jsonify({"status": "connected"})

# To make it simple and single page application from the backend all other URLs will be redirected
# To the keep alive
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect('/keepalive', code=200)

# ----------------------- Web Socket Communication ----------------------

# Web socket endpoint to receive Kafka data and publish it to front-end application
@socketio.on('connect')
def handle_connect():
    logMessage = 'WS:(Server) Connection Established'
    print(logMessage)
    socketio.emit('connect', logMessage)

@socketio.on('disconnect')
def handle_disconnect():
    logMessage = 'WS:(Server) Connection Lost'
    print(logMessage)

@socketio.on('test')
def test_connect():
    logMessage = 'WS:(Server) Test Connection'
    print(logMessage)
    socketio.emit('test', logMessage)

@socketio.on('json')
def handle_rsvp(offset):
    responseData = simulateRsvpMessage(offset)
    # responseData = getRsvpFromKafkaConsumer(offset)

    for message in responseData['messageList']: 
        socketio.emit('json', json.dumps(message))

    return responseData['end']

if __name__ == '__main__':
    socketio.run(app)
