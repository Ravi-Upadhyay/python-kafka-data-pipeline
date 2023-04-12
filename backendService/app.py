from flask import Flask

app = Flask(__name__)

@app.route("/")
def first_call():
    return "<p>App is running</p>"