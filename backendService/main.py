from flask import Flask

app = Flask(__name__)

@app.route("/")
def first_call():
    return "<p>Hello, World!</p>"