

DEFAULT_ENCODING = "utf-8"
FILE_LOCATION = "./streamMock/meetup.txt"

f = open(FILE_LOCATION, mode="rt", encoding=DEFAULT_ENCODING)
line = f.readline()
print(line)

# def openFileStream(): 
#     return open(FILE_LOCATION, mode="rt", encoding=DEFAULT_ENCODING)

# def closeFileStream(f):
#     close(f)
