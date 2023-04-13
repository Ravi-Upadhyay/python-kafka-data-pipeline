"""
Module: Main/Root Application
This is a single page application
Communicates with the front end over web socket
"""

from flask import Flask, jsonify, redirect
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='app', static_url_path="/app")
socketio = SocketIO(app, cors_allowed_origins='*')

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
    message = {"rsvp": "true"}
    print('Client connected')
    socketio.emit('data', message)

if __name__ == '__main__':
    socketio.run(app)