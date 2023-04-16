"""
Module: Main/Root Application
This is a single page application
Communicates with the front end over web socket
"""

from flask import Flask, jsonify, redirect
from kafka import KafkaConsumer
from flask_socketio import SocketIO

DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./streamMock/meetup.txt"
SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2

KAFKA_HOST = "localhost:9092"
KAFKA_TOPIC_INCOMING = "meetup-rsvp"
KAFKA_TOPIC_OUTGOING = "meetup-rsvp-true"

app = Flask(__name__, static_folder='app', static_url_path="/app")
socketio = SocketIO(app, cors_allowed_origins='*')

# Set up Kafka consumer
consumer = KafkaConsumer(KAFKA_TOPIC_OUTGOING, bootstrap_servers=[KAFKA_HOST], auto_offset_reset='earliest')

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

# Web socket endpoint to receive Kafka data and publish it to front-end application
@socketio.on('connect')
def test_connect():
    print('Connection Established')
    
    # for message in consumer:
    #     print(message)
    #     data = message.value.decode(DEFAULT_ENCODING)
    #     socketio.emit('data', data)

if __name__ == '__main__':
    socketio.run(app)