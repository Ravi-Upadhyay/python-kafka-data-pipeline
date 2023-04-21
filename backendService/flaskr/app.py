"""
Module: Main/Root Application
This is a single page application
Communicates with the front end over web socket
"""

from flask import Flask, jsonify, redirect

from flask_socketio import SocketIO

import eventlet

from constants import KAFKA_CONSUMER_MAX_POLL_RECORDS, DEFAULT_ENCODING

from data_pipeline_output import data_pipeline_output_main
from data_pipeline_input import data_pipeline_input_main
from data_pipeline_processor import data_pipeline_processor_main

def get_the_app():
    """
    FUNCTION: Create a Web Socket Enabled Flask App
    @returns Socketio, App
    """
    try: 
        app = Flask(__name__, static_folder='app', static_url_path="/app")

        # Initialize Socket - Kept commented debug mode initialization
        # socketio = SocketIO(app, cors_allowed_origins='*')
        socketio = SocketIO(app, cors_allowed_origins='*', logger=True, engineio_logger=True)

        def start_data_pipeline_input_as_service():
            """
            FUNCITON: start_data_pipeline_input_as_service(), Initiate data pipeline for input
            @returns: None
            @arguments: None
            TODO: Can be created as separated micro service / separate thread
            """
            data_pipeline_input_main()

        def start_data_pipeline_processor_as_service():
            """
            FUNCITON: start_data_pipeline_processor_as_service(), Initiate data pipeline for processing
            @returns: None
            @arguments: None
            TODO: Can be created as separated micro service / separate thread
            """
            data_pipeline_processor_main()

        def get_rsvp_from_kafka_consumer(offset):
            """
            FUNCITON: get_rsvp_from_kafka_consumer(), get rsvp data from kafka output pipeline
            @returns: List of events and end offset
            @arguments: start offset
            """
            start = int(offset)
            end = start + KAFKA_CONSUMER_MAX_POLL_RECORDS
            message_list = []
            events = data_pipeline_output_main(start)
            if events is not None:
                message_list = events
            return { 'message_list': message_list, 'end': end }

        @app.route("/keepalive")
        def keepalive():
            """
            HTTP: (FUNCTION)  /keepalive
            @returns: JSON health status
            @arguments: None
            """
            return jsonify({"status": "connected"})

        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def catch_all(path):
            """
            HTTP: (FUNCTION) For all routes, redirect to /keepalive
            Get RSVP Events Ouput Pipeline - i.e. With Rsvp True
            @returns: Redirect to /keepalive
            @arguments: None
            """
            return redirect('/keepalive', code=200)

        @socketio.on('connect')
        def handle_connect():
            """
            Web Socket: (FUNCTION) Generic Handler for connect
            @emits: Connection Establis log message
            @returns: None
            @arguments: None
            """
            log_message = 'WS:(Server) Connection Established'
            print(log_message)
            socketio.emit('connect', log_message)

        @socketio.on('disconnect')
        def handle_disconnect():
            """
            Web Socket: (FUNCTION) Generic Handler for Disconnect
            @emits: Connection Lost log message
            @returns: None
            @arguments: None
            """
            log_message = 'WS:(Server) Connection Lost'
            print(log_message)

        @socketio.on('test')
        def test_connect():
            """
            Web Socket: (FUNCTION) For Test Web Socket
            Get RSVP Events Ouput Pipeline - i.e. With Rsvp True
            @emits: Test Message from server for web socket connection
            @returns: None
            @arguments: None
            """
            log_message = 'WS:(Server) Test Connection'
            print(log_message)
            socketio.emit('test', log_message)

        @socketio.on('json')
        def handle_rsvp(offset):
            """
            Web Socket: (FUNCTION) For RSVP events
            Get RSVP Events Ouput Pipeline - i.e. With Rsvp True
            @emits: Rsvp Events
            @returns: End Offset
            @arguments: Start Offset
            """
            response_data = get_rsvp_from_kafka_consumer(offset)

            for message in response_data['message_list']: 
                socketio.emit('json', message.value.decode(DEFAULT_ENCODING))

            return response_data['end']
        start_data_pipeline_input_as_service()
        start_data_pipeline_processor_as_service()
        return {"app": app, "socketio": socketio}
    except: 
        print('Error: get_the_app(), could not create app')

def iniate_server():
    resources = get_the_app()
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), resources['socketio'].run(resources['app']))

if __name__ == '__main__':
    iniate_server()
