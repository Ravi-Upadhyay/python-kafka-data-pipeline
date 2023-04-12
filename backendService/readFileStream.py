from time import sleep

DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./streamMock/meetup.txt"
SLEEP_TIME_BEFORE_READ_NEXT_LINE = 2

# f = open(FILE_LOCATION, mode="rt", encoding=DEFAULT_ENCODING)
# line = f.readline()
# print(line)

def processLine(l):
    print(l)
    sleep(SLEEP_TIME_BEFORE_READ_NEXT_LINE)


with open(FILE_LOCATION, mode="rt", encoding=DEFAULT_ENCODING) as openfileobject:
    for line in openfileobject:
        processLine(line)

# def openFileStream(): 
#     return open(FILE_LOCATION, mode="rt", encoding=DEFAULT_ENCODING)

# def closeFileStream(f):
#     close(f)
