def declareConstants():
    global DEFAULT_ENCODING
    global FILE_LOCATION
    global SLEEP_TIME_BEFORE_READ_NEXT_LINE

    global KAFKA_HOST
    global KAFKA_TOPIC_INCOMING
    global KAFKA_TOPIC_OUTGOING
    
    DEFAULT_ENCODING = "utf-8"
    FILE_LOCATION = "./streamMock/meetup.txt"
    SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2

    KAFKA_HOST = "localhost:9092"
    KAFKA_TOPIC_INCOMING = "meetup-rsvp"
    KAFKA_TOPIC_OUTGOING = "meetup-rsvp-true"

if __name__ == '__main__':
    declareConstants()