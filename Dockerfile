
FROM python:latest
RUN apt-get update; apt-get install vim tmux -y
RUN pip3 install kafka-python flask-expects-json Flask[async] flask_socketio gunicorn  eventlet
ADD ../backendService/  /backendService
CMD ["/bin/sleep","1000000"]
ENTRYPOINT ["/usr/local/bin/python3","/backendService/flaskr/app.py"]
