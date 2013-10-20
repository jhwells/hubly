#!/usr/bin/python
from flask import Flask
from flask import jsonify
from sendHub import calculateRoutes
from sendHub import backend_resources

app = Flask(__name__)

@app.route('/')
def index():
    return "sendHub"


@app.route('/relays/routes', methods=['GET'])
def calculate_routes():
    pass

@app.route('/relays', methods=['GET'])
def get_relays():
    return jsonify(resources=backend_resources)

if __name__ == '__main__':
    app.run(debug=True)
