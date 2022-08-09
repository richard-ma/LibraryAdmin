from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<H1>hello</H1>"
