from os import listdir
from os.path import isfile, join, splitext

import face_recognition
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

# Create flask app
app = Flask(__name__)
CORS(app)

# <Picture functions> #


@app.route('/', methods=['GET'])
def web_run():
    return "running"


if __name__ == "__main__":
    print("Starting by generating encodings for found images...")
    web_run()
    print("Starting WebServer...")
    app.run(host='0.0.0.0', port=8888, debug=False)
